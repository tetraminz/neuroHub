from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score

mne = pytest.importorskip("mne")
read_raw_edf = mne.io.read_raw_edf


def test_bigp3bci_edf_properties() -> None:
    """Ensure bigP3BCI sample has expected metadata."""
    edf_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / (
            "bigp3bci-an-open-diverse-and-machine-learning-ready-"
            "p300-based-brain-computer-interface-dataset-1.0.0"
        )
        / "bigP3BCI-data"
        / "StudyA"
        / "A_01"
        / "SE001"
        / "Train"
        / "CB"
        / "A_01_SE001_CB_Train01.edf"
    )
    if not edf_path.exists():
        pytest.skip(f"{edf_path} not found")

    raw = read_raw_edf(edf_path, preload=False, verbose=False)

    assert raw.info["sfreq"] == pytest.approx(256.0, rel=1e-4)
    assert 60 <= raw.info["nchan"] <= 128


def test_bigp3bci_real_data_lda() -> None:
    """LDA on sample recording should exceed 60 % accuracy."""
    edf_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / (
            "bigp3bci-an-open-diverse-and-machine-learning-ready-"
            "p300-based-brain-computer-interface-dataset-1.0.0"
        )
        / "bigP3BCI-data"
        / "StudyA"
        / "A_01"
        / "SE001"
        / "Train"
        / "CB"
        / "A_01_SE001_CB_Train01.edf"
    )
    raw = read_raw_edf(edf_path, preload=True, verbose=False)

    stim_begin = raw.get_data(picks=["StimulusBegin"])[0]
    stim_type = raw.get_data(picks=["StimulusType"])[0].astype(int)
    onsets = np.where(stim_begin > 0)[0]
    events = np.c_[onsets, np.zeros(len(onsets), int), stim_type[onsets]]

    raw.pick("eeg")
    raw.filter(0.1, 30, verbose=False)
    raw.resample(128, npad="auto", verbose=False)

    epochs = mne.Epochs(
        raw,
        events,
        event_id={"non": 0, "target": 1},
        tmin=-0.2,
        tmax=0.8,
        baseline=None,
        preload=True,
        verbose=False,
    )
    window = epochs.time_as_index([0.25, 0.45])
    X = epochs.get_data()[:, :, window[0] : window[1]].reshape(len(epochs), -1)
    y = epochs.events[:, 2]
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    clf = LinearDiscriminantAnalysis()
    scores = cross_val_score(clf, X, y, cv=cv)

    assert np.mean(scores) >= 0.60
