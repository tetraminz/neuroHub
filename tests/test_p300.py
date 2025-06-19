"""Smoke test: synthetic P300‑like data → LDA ≥ 0.60 accuracy."""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def test_synthetic_p300_lda():
    # Simulate imbalance similar to P300 (≈1:6)
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
    assert mean_acc >= 0.60, "LDA baseline should exceed 60 % on toy data"

