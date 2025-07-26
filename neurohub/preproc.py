"""Preprocessing utilities."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import mne
import numpy as np
from scipy.signal import firwin, freqz

from .config import DEFAULTS


def apply_bandpass(
    raw: mne.io.BaseRaw,
    l_freq: float = 0.1,
    h_freq: float = 30.0,
    picks: str | Iterable[str] | None = "data",
) -> mne.io.BaseRaw:
    """Apply band-pass filter in-place."""
    # Демонстрируем фильтр 0.1-30 Гц
    raw.filter(l_freq, h_freq, picks=picks, fir_design="firwin", verbose=False)
    return raw


def bandpass(
    raw: mne.io.BaseRaw,
    l_freq: float = DEFAULTS["l_freq"],
    h_freq: float = DEFAULTS["h_freq"],
) -> mne.io.BaseRaw:
    """Legacy alias for ``apply_bandpass``."""
    return apply_bandpass(raw, l_freq, h_freq)


def plot_filter_response(l_freq: float, h_freq: float, sfreq: float) -> plt.Figure:
    """Plot the frequency response of an FIR band-pass filter."""
    numtaps = int(sfreq * 3)
    fir = firwin(numtaps, [l_freq, h_freq], pass_zero=False, fs=sfreq)
    w, h = freqz(fir, worN=8000, fs=sfreq)
    fig, ax = plt.subplots()
    ax.plot(w, 20 * np.log10(np.abs(h)))
    ax.axvline(l_freq, ls="--", color="g")
    ax.axvline(h_freq, ls="--", color="r")
    ax.set(xlabel="Frequency (Hz)", ylabel="Gain (dB)")
    ax.set_title(f"Band-pass {l_freq}-{h_freq} Hz")
    return fig


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
