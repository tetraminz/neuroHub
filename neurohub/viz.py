"""Visualization helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt
import mne
import numpy as np


def plot_erp(epochs: mne.Epochs) -> plt.Figure:
    """Plot target vs non-target ERP."""
    fig, ax = plt.subplots()
    for label, color in zip([1, 0], ["tab:red", "tab:blue"]):
        evoked = epochs[label].average()
        evoked.plot(axes=ax, show=False, time_unit="s", spatial_colors=False)
    ax.legend(["target", "non"])
    return fig


def plot_scalp(weights: np.ndarray, info: mne.Info) -> plt.Figure:
    """Plot classifier weights on sensor topography."""
    fig, ax = plt.subplots()
    mne.viz.plot_topomap(weights, info, axes=ax, show=False)
    return fig
