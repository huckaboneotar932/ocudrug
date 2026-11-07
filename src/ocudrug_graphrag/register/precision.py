"""Precision@K.

Ref: Table 1 (Precision@10 across UM/RB/OAL).
"""

from __future__ import annotations

from collections.abc import Iterable


def precision_at_k(ranked: list[str], positives: Iterable[str], k: int) -> float:
    if k <= 0:
        return 0.0
    positive_set = set(positives)
    top = ranked[:k]
    hits = sum(1 for d in top if d in positive_set)
    return hits / float(k)
