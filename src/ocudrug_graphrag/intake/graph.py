"""Typed ocular knowledge-(sub)graph backed by a directed multigraph.

Ref: §6.1 (node types Phi, edge-type map phi); §6.3 (2-hop subgraph).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import cast

import networkx as nx

from ocudrug_graphrag.casework.types import KnowledgeGraph, Subtype

NodeType = str
RELATION_DISEASE_GENE = "disease_gene"
RELATION_GENE_DRUG = "gene_drug"
RELATION_DRUG_DISEASE = "drug_disease"


@dataclass(frozen=True, slots=True)
class TypedEdge:
    src: str
    dst: str
    relation: str
    mechanism: str

    def edge_id(self) -> str:
        return f"{self.src}|{self.relation}|{self.dst}"


@dataclass(slots=True)
class OcularSubgraph:
    kg: KnowledgeGraph
    subtype: Subtype
    root: str
    graph: nx.MultiDiGraph[str] = field(default_factory=nx.MultiDiGraph)

    def add_edge(self, edge: TypedEdge) -> None:
        self.graph.add_edge(edge.src, edge.dst, relation=edge.relation, mechanism=edge.mechanism)

    def node_count(self) -> int:
        return int(self.graph.number_of_nodes())

    def edge_count(self) -> int:
        return int(self.graph.number_of_edges())

    def drugs(self) -> list[str]:
        out: list[str] = [n for n in self.graph.nodes if str(n).startswith("drug:")]
        return sorted(out)

    def paths_to_root(self, drug: str, max_len: int) -> list[list[TypedEdge]]:
        raw = nx.all_simple_edge_paths(self.graph, drug, self.root, cutoff=max_len)
        paths: list[list[TypedEdge]] = []
        for edge_path in raw:
            chain: list[TypedEdge] = []
            for u, v, key in edge_path:
                data = self.graph.get_edge_data(u, v, key)
                chain.append(
                    TypedEdge(
                        src=str(u),
                        dst=str(v),
                        relation=str(data["relation"]),
                        mechanism=str(data["mechanism"]),
                    )
                )
            paths.append(chain)
        return paths

    def edge_ids(self) -> list[str]:
        ids: list[str] = []
        for u, v, data in self.graph.edges(data=True):
            ids.append(f"{u}|{data['relation']}|{v}")
        return sorted(ids)

    def fingerprint(self) -> str:
        payload = ";".join(self.edge_ids())
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def degree_capped_neighbors(graph: nx.MultiDiGraph[str], node: str, degree_cap: int) -> list[str]:
    succ = cast(list[str], sorted(str(n) for n in graph.successors(node)))
    pred = cast(list[str], sorted(str(n) for n in graph.predecessors(node)))
    merged = sorted(set(succ) | set(pred))
    return merged[:degree_cap]
