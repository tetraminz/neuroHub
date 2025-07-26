"""Feature extraction and classification."""

from __future__ import annotations

import mne
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score

from .config import DEFAULTS


def extract_features(
    epochs: mne.Epochs,
    window: tuple[float, float] = DEFAULTS["feature_window"],
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorize the given time window from epochs."""
    idx = epochs.time_as_index(window)
    X = epochs.get_data()[:, :, idx[0] : idx[1]].reshape(len(epochs), -1)
    y = epochs.events[:, 2]
    return X, y


def lda_cv(X: np.ndarray, y: np.ndarray, cv_splits: int = 5) -> float:
    """Cross-validate an LDA classifier and return mean accuracy."""
    cv = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=42)
    clf = LinearDiscriminantAnalysis()
    scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
    return float(scores.mean())
