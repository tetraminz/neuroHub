"""Ensure filtering preserves desired frequency band."""

from __future__ import annotations

import mne
import numpy as np

from neurohub.preproc import apply_bandpass, bandpass


def test_bandpass_frequency_content() -> None:
    """Signal at 1 Hz remains while 40 Hz attenuates."""
    sfreq = 256
    times = np.arange(0, 2, 1 / sfreq)
    sig = np.sin(2 * np.pi * 1 * times) + 0.5 * np.sin(2 * np.pi * 40 * times)
    info = mne.create_info(["eeg"], sfreq, ch_types="eeg")
    raw = mne.io.RawArray(sig[np.newaxis] * 1e-6, info)

    bandpass(raw, 0.1, 30)
    data = raw.get_data()[0]
    fft = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1 / sfreq)
    low = fft[freqs == 1].item()
    high = fft[freqs == 40].item()
    assert low > high


def test_apply_bandpass_alias() -> None:
    """apply_bandpass should behave like bandpass."""
    sfreq = 256
    times = np.arange(0, 1, 1 / sfreq)
    sig = np.sin(2 * np.pi * 10 * times)
    info = mne.create_info(["eeg"], sfreq, ch_types="eeg")
    raw = mne.io.RawArray(sig[np.newaxis] * 1e-6, info)
    apply_bandpass(raw, 0.1, 30)
    assert np.isclose(raw.info["lowpass"], 30)
