"""Preprocessing utilities."""

from __future__ import annotations

from typing import Iterable

import mne

from .config import DEFAULTS


def bandpass(
    raw: mne.io.BaseRaw,
    l_freq: float = DEFAULTS["l_freq"],
    h_freq: float = DEFAULTS["h_freq"],
) -> mne.io.BaseRaw:
    """Apply band-pass filter in-place and return raw."""
    raw.filter(l_freq, h_freq, fir_design="firwin", verbose=False)
    return raw


def notch(
    raw: mne.io.BaseRaw, freqs: Iterable[float] = (50.0, 100.0)
) -> mne.io.BaseRaw:
    """Notch filter power-line noise."""
    raw.notch_filter(freqs=freqs, verbose=False)
    return raw


def decimate(
    raw: mne.io.BaseRaw, sfreq: int = DEFAULTS["resample_sfreq"]
) -> mne.io.BaseRaw:
    """Resample raw data to `sfreq`."""
    raw.resample(sfreq, verbose=False)
    return raw


def make_epochs(
    raw: mne.io.BaseRaw,
    tmin: float = DEFAULTS["tmin"],
    tmax: float = DEFAULTS["tmax"],
) -> mne.Epochs:
    """Create epochs from raw annotations."""
    if not len(raw.annotations):
        raise ValueError("Raw object lacks annotations")
    desc_map = {"non": 0, "target": 1}
    events, event_id = mne.events_from_annotations(raw, event_id=desc_map)
    epochs = mne.Epochs(
        raw,
        events,
        event_id=event_id,
        tmin=tmin,
        tmax=tmax,
        baseline=None,
        event_repeated="drop",
        preload=True,
        verbose=False,
    )
    return epochs
