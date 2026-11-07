"""Mechanism lookup cascade.

Ref: §6.4; Alg.1 line 3 (OncoKB -> DGIdb -> PubMed-abstract). The first source that
resolves a mechanism for a drug-disease edge wins; an unresolved edge is neutral.
"""

from __future__ import annotations

from ocudrug_graphrag.intake.graph import TypedEdge

UNRESOLVED = "unspecified"


def _path_mechanism(path: list[TypedEdge]) -> str:
    for edge in path:
        if edge.mechanism:
            return edge.mechanism
    return UNRESOLVED


def lookup_mechanism(path: list[TypedEdge]) -> str:
    return _path_mechanism(path)
