"""Stage 1 ocular subgraph distillation.

Ref: §6.3; Alg.1 lines 1-5. MONDO/DOID-anchored breadth-first expansion to depth h
with a typed-degree cap; rare nodes with <=5 outgoing edges trigger a k=3 widening.
"""

from __future__ import annotations

import networkx as nx

from ocudrug_graphrag.casework.log import get_logger
from ocudrug_graphrag.intake.graph import OcularSubgraph, TypedEdge

_LOG = get_logger(__name__)
EDGE_BOUND = 160_000


def _bfs_nodes(graph: nx.MultiDiGraph[str], root: str, depth_h: int, degree_cap: int) -> set[str]:
    undirected = graph.to_undirected(as_view=True)
    frontier: set[str] = {root}
    seen: set[str] = {root}
    for _ in range(depth_h):
        nxt: set[str] = set()
        for node in frontier:
            neighbours = sorted(str(n) for n in undirected.neighbors(node))
            cap = degree_cap if len(neighbours) > 5 else degree_cap * 3
            for nb in neighbours[:cap]:
                if nb not in seen:
                    seen.add(nb)
                    nxt.add(nb)
        frontier = nxt
    return seen


def distill_subgraph(
    source: OcularSubgraph, depth_h: int = 2, degree_cap: int = 64
) -> OcularSubgraph:
    keep = _bfs_nodes(source.graph, source.root, depth_h, degree_cap)
    out = OcularSubgraph(kg=source.kg, subtype=source.subtype, root=source.root)
    for node in keep:
        out.graph.add_node(node, **source.graph.nodes[node])
    for u, v, data in source.graph.edges(data=True):
        if str(u) in keep and str(v) in keep:
            out.add_edge(TypedEdge(str(u), str(v), str(data["relation"]), str(data["mechanism"])))
    if out.edge_count() > EDGE_BOUND:
        raise ValueError(f"distilled edge count {out.edge_count()} exceeds bound {EDGE_BOUND}")
    _LOG.debug(
        "distilled %s/%s: %d nodes %d edges",
        source.kg,
        source.subtype,
        out.node_count(),
        out.edge_count(),
    )
    return out
