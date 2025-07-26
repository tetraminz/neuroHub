"""Top-level API for the neurohub package."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import mne

from . import config, features, io, preproc, viz
from .config import DEFAULTS
from .features import extract_features, lda_cv
from .io import load_bnci, load_raw, synthetic
from .preproc import bandpass, decimate, make_epochs, notch
from .viz import plot_erp, plot_scalp

__all__ = [
    "load_raw",
    "load_bnci",
    "synthetic",
    "bandpass",
    "notch",
    "decimate",
    "make_epochs",
    "extract_features",
    "lda_cv",
    "plot_erp",
    "plot_scalp",
    "run_p300_pipeline",
    "DEFAULTS",
]


def run_p300_pipeline(data_path: Optional[str], out_dir: str) -> float:
    """Run the full P300 workflow and return mean CV accuracy."""
    if data_path:
        raw = load_raw(data_path)
    else:
        raw = synthetic()

    bandpass(raw)
    decimate(raw)
    epochs = make_epochs(raw)
    X, y = extract_features(epochs)
    acc = lda_cv(X, y)
    print(f"Mean CV accuracy: {acc:.3f}")

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    fig = plot_erp(epochs)
    fig.savefig(out / "erp.png")
    plt.close(fig)
    return acc
