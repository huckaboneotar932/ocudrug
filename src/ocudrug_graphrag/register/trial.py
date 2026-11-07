"""Trial@K against the ClinicalTrials.gov active/completed window.

Ref: Table 1/Table 5 (Trial@20 hit-rate). Fraction of the Top-K ranking that maps to
an active or completed trial in the look-back window.
"""

from __future__ import annotations

from collections.abc import Iterable


def trial_at_k(ranked: list[str], trial_drugs: Iterable[str], k: int) -> float:
    if k <= 0:
        return 0.0
    trial_set = set(trial_drugs)
    top = ranked[:k]
    return sum(1 for d in top if d in trial_set) / float(k)
