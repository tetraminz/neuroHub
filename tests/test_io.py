"""Test synthetic raw generation."""

from __future__ import annotations

import mne

from neurohub.io import synthetic


def test_synthetic_raw_properties() -> None:
    """Synthetic data should have 20 channels and 60 s duration."""
    raw = synthetic()
    assert isinstance(raw, mne.io.BaseRaw)
    assert raw.info["nchan"] == 20
    assert raw.times[-1] >= 59
