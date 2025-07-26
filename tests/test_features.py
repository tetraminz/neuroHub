"""Check LDA classification on synthetic P300."""

from __future__ import annotations

from neurohub.features import extract_features, lda_cv
from neurohub.io import synthetic
from neurohub.preproc import bandpass, decimate, make_epochs


def test_lda_on_synthetic() -> None:
    """Pipeline on synthetic data should exceed 60 % accuracy."""
    raw = synthetic()
    bandpass(raw)
    decimate(raw)
    epochs = make_epochs(raw)
    X, y = extract_features(epochs)
    acc = lda_cv(X, y)
    assert acc >= 0.60
