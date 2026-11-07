"""Nonparametric bootstrap confidence intervals.

Ref: §6.5/§6.8 (B=200 percentile bootstrap); §3.2 (paired-bootstrap Delta CI).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ocudrug_graphrag.casework.seed import stable_rng


def bootstrap_ci(
    sample: list[float], b: int = 200, *, tag: str = "ci", alpha: float = 0.05
) -> tuple[float, float, float]:
    arr = np.asarray(sample, dtype=np.float64)
    if arr.size == 0:
        return (0.0, 0.0, 0.0)
    rng = stable_rng("bootstrap", tag, arr.size, b)
    means = np.empty(b, dtype=np.float64)
    for i in range(b):
        idx = rng.integers(0, arr.size, arr.size)
        means[i] = float(np.mean(arr[idx]))
    low = float(np.percentile(means, 100 * alpha / 2))
    high = float(np.percentile(means, 100 * (1 - alpha / 2)))
    return (float(np.mean(arr)), low, high)


def paired_bootstrap_delta(
    ours: list[float], baseline: list[float], b: int = 200, *, tag: str = "delta"
) -> tuple[float, float, float, bool]:
    a = np.asarray(ours, dtype=np.float64)
    c = np.asarray(baseline, dtype=np.float64)
    diff = a - c
    rng = stable_rng("paired", tag, diff.size, b)
    deltas: NDArray[np.float64] = np.empty(b, dtype=np.float64)
    for i in range(b):
        idx = rng.integers(0, diff.size, diff.size)
        deltas[i] = float(np.mean(diff[idx]))
    low = float(np.percentile(deltas, 2.5))
    high = float(np.percentile(deltas, 97.5))
    excludes_zero = low > 0.0 or high < 0.0
    return (float(np.mean(diff)), low, high, excludes_zero)
