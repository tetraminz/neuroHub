"""Smoke tests for P300 classification."""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score


def test_synthetic_p300_lda():
    """Balanced toy data should yield >=60 % accuracy."""
    n_target = 200
    n_nontarget = n_target * 6
    X, y = make_classification(
        n_samples=n_target + n_nontarget,
        n_features=20,
        n_informative=6,
        n_redundant=2,
        n_clusters_per_class=1,
        weights=[n_target / (n_target + n_nontarget)],
        class_sep=1.0,
        random_state=42,
    )

    clf = LinearDiscriminantAnalysis()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")

    mean_acc = np.mean(scores)
    print(f"Mean CV accuracy on synthetic P300 data: {mean_acc:.3f}")
    assert mean_acc >= 0.60, "LDA baseline should exceed 60% on toy data"


def test_extreme_imbalance():
    """Classifier should cope with severe class imbalance."""
    n_target = 100
    n_nontarget = n_target * 10
    X, y = make_classification(
        n_samples=n_target + n_nontarget,
        n_features=20,
        n_informative=6,
        n_redundant=2,
        n_clusters_per_class=1,
        weights=[n_target / (n_target + n_nontarget)],
        class_sep=1.0,
        random_state=0,
    )

    clf = LinearDiscriminantAnalysis()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    scores = cross_val_score(clf, X, y, cv=cv)

    assert np.mean(scores) >= 0.60


def test_missing_channels():
    """Dropping features mimics missing EEG channels."""
    X, y = make_classification(
        n_samples=400,
        n_features=16,
        n_informative=5,
        n_redundant=1,
        n_clusters_per_class=1,
        random_state=42,
    )
    X_drop = X[:, 2:]

    clf = LinearDiscriminantAnalysis()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(clf, X_drop, y, cv=cv)

    assert np.mean(scores) >= 0.60
