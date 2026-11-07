"""Verifiable forms of the appendix theorems.

Ref: Appendix A. Thm.1 Eq.(6) Tier-3 reliability lower bound; Thm.2 mechanism-path
Pareto-optimality; Thm.4 Eq.(7) hybrid variance reduction. Thm.3 (byte-identical
re-execution) is realised by custody.ledger.record_digest.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Tier3Bound:
    lower_bound: float
    fpr_suppression: float


def tier3_lower_bound(p_star: float = 0.65, q_star: float = 0.18) -> Tier3Bound:
    p3 = p_star**3
    q3 = q_star**3
    bound = 1.0 - 3.0 * q3 / (q3 + p3)
    suppression = q_star / q3
    return Tier3Bound(lower_bound=bound, fpr_suppression=suppression)


@dataclass(frozen=True, slots=True)
class VarianceBound:
    reduced_upper_bound: float
    coefficient: float


def variance_reduction_bound(
    min_var: float, delta: float = 0.18, eps: float = 0.062
) -> VarianceBound:
    reduction = (2.0 / 9.0) * (1.0 - eps) * delta**2
    reduced = min_var - reduction
    coefficient = reduced / min_var if min_var > 0.0 else 0.0
    return VarianceBound(reduced_upper_bound=reduced, coefficient=coefficient)


def _dominates(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return a[0] >= b[0] and a[1] >= b[1] and (a[0] > b[0] or a[1] > b[1])


def pareto_dominance_check(
    operating: tuple[float, float], alternatives: dict[str, tuple[float, float]]
) -> bool:
    return all(_dominates(operating, alt) for alt in alternatives.values())
