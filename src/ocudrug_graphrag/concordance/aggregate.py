"""Stage 3 cross-source concordance.

Ref: §6.5 Eq.(1) sigma(d,t); Eq.(5) concordance(d,D); Alg.2 lines 1-5. Membership is
counted with compensated summation so the aggregate is bit-stable for re-execution.
"""

from __future__ import annotations

import math
from itertools import combinations

from ocudrug_graphrag.casework.types import KnowledgeGraph
from ocudrug_graphrag.register.jaccard import jaccard_topk

TopKLists = dict[KnowledgeGraph, list[str]]


def union_topk(per_kg_topk: TopKLists) -> list[str]:
    out: set[str] = set()
    for lst in per_kg_topk.values():
        out.update(lst)
    return sorted(out)


def kg_agreement_fraction(drug: str, per_kg_topk: TopKLists) -> float:
    indicators = [1.0 if drug in lst else 0.0 for lst in per_kg_topk.values()]
    return math.fsum(indicators) / float(len(per_kg_topk))


def reliability_tier(drug: str, per_kg_topk: TopKLists) -> int:
    return sum(1 for lst in per_kg_topk.values() if drug in lst)


def mean_pairwise_jaccard(per_kg_full: TopKLists, k: int) -> float:
    pairs = list(combinations(sorted(per_kg_full), 2))
    if not pairs:
        return 0.0
    values = [jaccard_topk(per_kg_full[a], per_kg_full[b], k) for a, b in pairs]
    return math.fsum(values) / float(len(pairs))


def concordance_sigma(
    drug: str, per_kg_full: TopKLists, *, alpha: float = 0.6, k: int = 20
) -> float:
    topk = {kg: lst[:k] for kg, lst in per_kg_full.items()}
    membership = kg_agreement_fraction(drug, topk)
    return membership + alpha * mean_pairwise_jaccard(per_kg_full, k)
