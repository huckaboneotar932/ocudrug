"""Top-K Jaccard overlap.

Ref: §6.5 Eq.(1) pairwise term; Table 3 (Top-20 Jaccard across KGs).
"""

from __future__ import annotations


def jaccard_topk(list_a: list[str], list_b: list[str], k: int) -> float:
    set_a = set(list_a[:k])
    set_b = set(list_b[:k])
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / float(len(union))
