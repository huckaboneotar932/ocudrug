"""Stage 2 mechanism-typed path retrieval.

Ref: Alg.1 lines 6-13. Per candidate drug: enumerate paths to the disease root
(length <= L), score each path by Eq.(3), retain the top-M, and reduce by Eq.(4).
"""

from __future__ import annotations

import math
from collections.abc import Callable

from ocudrug_graphrag.casework.types import Candidate, Subtype
from ocudrug_graphrag.intake.graph import OcularSubgraph, TypedEdge
from ocudrug_graphrag.workup.mechanism import lookup_mechanism
from ocudrug_graphrag.workup.score import drug_score, path_mechanism_score


def retrieve_paths(
    subgraph: OcularSubgraph,
    subtype: Subtype,
    *,
    path_cap_l: int = 3,
    top_m: int = 50,
    scorer: Callable[[OcularSubgraph, list[TypedEdge]], float],
) -> list[Candidate]:
    out: list[Candidate] = []
    for drug in subgraph.drugs():
        paths = subgraph.paths_to_root(drug, path_cap_l)
        if not paths:
            continue
        scored: list[tuple[float, str]] = []
        for path in paths:
            mechanism = lookup_mechanism(path)
            logit = float(scorer(subgraph, path))
            if not math.isfinite(logit):
                raise ValueError("Path scorer returned a non-finite value.")
            scored.append((path_mechanism_score(logit, mechanism, subtype), mechanism))
        scored.sort(key=lambda t: t[0], reverse=True)
        scored = scored[:top_m]
        best_score = drug_score([s for s, _ in scored])
        best_mechanism = next(m for s, m in scored if s == best_score)
        out.append(
            Candidate(
                drug=drug[len("drug:") :],
                score=best_score,
                mechanism=best_mechanism,
                paths=len(paths),
            )
        )
    out.sort(key=lambda c: (-c.score, c.drug))
    return out
