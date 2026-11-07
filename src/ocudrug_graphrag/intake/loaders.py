"""Gated loaders for the public knowledge graphs.

Ref: Table 7 dataset registry. These adapters are intentionally inert: the upstream
dumps are access-controlled and not redistributed with this release. Point each loader
at a local copy obtained from the documented source to enable real-data runs.
"""

from __future__ import annotations

from pathlib import Path

from ocudrug_graphrag.casework.types import KnowledgeGraph, Subtype
from ocudrug_graphrag.intake.graph import OcularSubgraph

SOURCE_URL: dict[KnowledgeGraph, str] = {
    "PrimeKG": "https://doi.org/10.7910/DVN/IXA7BM",
    "Hetionet": "https://het.io",
    "DRKG": "https://github.com/gnn4dr/DRKG",
}


def load_real_subgraph(kg: KnowledgeGraph, subtype: Subtype, dump_dir: Path) -> OcularSubgraph:
    raise NotImplementedError(
        f"{kg} loader is gated; place the dump from {SOURCE_URL[kg]} under {dump_dir} "
        "and implement the project-specific parser."
    )
