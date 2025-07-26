"""Test synthetic raw generation."""

from __future__ import annotations

import mne
import pytest

from neurohub.io import list_dataset_structure, load_bigp3bci, synthetic


def test_synthetic_raw_properties() -> None:
    """Synthetic data should have 20 channels and 60 s duration."""
    raw = synthetic()
    assert isinstance(raw, mne.io.BaseRaw)
    assert raw.info["nchan"] == 20
    assert raw.times[-1] >= 59


def test_list_dataset_structure(tmp_path) -> None:
    """Listing should parse study/subject/session folders."""
    p = tmp_path / "StudyA" / "S1" / "SE001" / "Train" / "CB"
    p.mkdir(parents=True)
    f = p / "rec.edf"
    f.touch()
    df = list_dataset_structure(tmp_path)
    assert len(df) == 1
    assert df.iloc[0]["study"] == "StudyA"


def test_load_bigp3bci_missing(tmp_path) -> None:
    """Missing EDF path should raise a clear error."""
    with pytest.raises(FileNotFoundError):
        load_bigp3bci(tmp_path / "nofile.edf")
