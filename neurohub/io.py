"""Input/output helpers for EEG data."""

from __future__ import annotations

from pathlib import Path

import mne
import numpy as np
import pandas as pd


def load_raw(path: str | Path) -> mne.io.BaseRaw:
    """Load a raw recording from FIF or EDF."""
    path = Path(path)
    if path.suffix == ".fif":
        raw = mne.io.read_raw_fif(path, preload=True, verbose=False)
    else:
        raw = mne.io.read_raw_edf(path, preload=True, verbose=False)
    return raw


def load_bnci() -> mne.io.BaseRaw:
    """Load a small BNCI example dataset via MNE."""
    try:
        from mne.datasets import sample
    except Exception as exc:  # pragma: no cover - import safeguard
        raise RuntimeError("MNE sample dataset not available") from exc
    sample_path = Path(sample.data_path()) / "MEG" / "sample" / "sample_audvis_raw.fif"
    return mne.io.read_raw_fif(sample_path, preload=True, verbose=False)


def synthetic(duration: float = 60.0, sfreq: int = 256) -> mne.io.Raw:
    """Generate synthetic P300-like EEG."""
    ch_names = [f"EEG{i:02d}" for i in range(20)]
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")
    n_samples = int(duration * sfreq)
    rng = np.random.default_rng(42)
    data = 1e-6 * rng.standard_normal((len(ch_names), n_samples))
    raw = mne.io.RawArray(data, info)

    n_target = 20
    n_non = 120
    times = rng.choice(
        np.arange(sfreq, n_samples - sfreq), n_target + n_non, replace=False
    )
    labels = np.array([1] * n_target + [0] * n_non)
    rng.shuffle(labels)
    amp = np.linspace(5e-6, 1e-6, len(ch_names))[:, None]
    width = int(0.1 * sfreq)
    gauss = np.exp(-0.5 * ((np.arange(width) - width // 2) / (0.05 * sfreq)) ** 2)
    for t, lbl in zip(times, labels):
        if lbl == 1:
            start = t + int(0.3 * sfreq) - width // 2
            if 0 <= start < n_samples - width:
                raw._data[:, start : start + width] += amp * gauss
    desc = np.where(labels == 1, "target", "non")
    onsets = times / sfreq
    durations = np.full_like(onsets, 0.0, dtype=float)
    anns = mne.Annotations(onsets, durations, desc)
    raw.set_annotations(anns)
    return raw


def load_bigp3bci(path: Path) -> mne.io.BaseRaw:
    """Load a BigP3BCI EDF file, raising an informative error if missing."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Please run `dvc pull`.")
    return mne.io.read_raw_edf(path, preload=True, verbose=False)


def list_dataset_structure(root: Path) -> pd.DataFrame:
    """Return a table describing all EDF files under ``root``."""
    root = Path(root)
    rows = []
    for edf in root.glob("**/*.edf"):
        rel = edf.relative_to(root)
        parts = rel.parts
        if len(parts) < 6:
            continue
        rows.append(
            {
                "study": parts[0],
                "subject": parts[1],
                "session": parts[2],
                "subset": parts[3],
                "paradigm": parts[4],
                "file": parts[5],
                "path": edf,
            }
        )
    return pd.DataFrame(rows)
