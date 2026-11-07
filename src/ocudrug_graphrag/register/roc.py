"""ROC-AUC via the rank-sum identity, with tie-aware averaged ranks.

Ref: Table 1 (ROC-AUC column).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def _average_ranks(scores: NDArray[np.float64]) -> NDArray[np.float64]:
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores), dtype=np.float64)
    sorted_scores = scores[order]
    i = 0
    n = len(scores)
    while i < n:
        j = i
        while j + 1 < n and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def roc_auc(scores: list[float], labels: list[int]) -> float:
    arr = np.asarray(scores, dtype=np.float64)
    lab = np.asarray(labels, dtype=np.int64)
    n_pos = int(np.sum(lab == 1))
    n_neg = int(np.sum(lab == 0))
    if n_pos == 0 or n_neg == 0:
        return 0.5
    ranks = _average_ranks(arr)
    rank_sum_pos = float(np.sum(ranks[lab == 1]))
    return (rank_sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)
