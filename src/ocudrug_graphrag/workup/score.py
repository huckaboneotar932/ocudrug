"""Stage 2 scoring functions.

Ref: §6.4 Eq.(3) s(d,D,m)=sigmoid(NBFNet_logit)*compat(m,D); Eq.(4) s(d,D)=max over paths.
"""

from __future__ import annotations

import math

from ocudrug_graphrag.casework.types import Subtype
from ocudrug_graphrag.workup.compat import compat


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def path_mechanism_score(logit: float, mechanism: str, subtype: Subtype) -> float:
    return sigmoid(logit) * compat(mechanism, subtype)


def drug_score(path_scores: list[float]) -> float:
    return max(path_scores) if path_scores else 0.0
