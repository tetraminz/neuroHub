from __future__ import annotations

import os
from pathlib import Path

import pytest

mne = pytest.importorskip("mne")
read_raw_edf = mne.io.read_raw_edf


def test_bigp3bci_edf_properties() -> None:
    """Ensure bigP3BCI sample has expected metadata."""
    root = Path(os.environ.get("NEURO_DATA_ROOT", str(Path.home() / "neuro-data")))
    edf_path = (
        root
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

    assert raw.info["sfreq"] == 256.0
    assert 60 <= raw.info["nchan"] <= 128
