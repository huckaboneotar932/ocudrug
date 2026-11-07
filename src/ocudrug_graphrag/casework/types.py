"""Shared domain vocabulary and record types.

Ref: §6.1 (𝒯, mechanism set 𝓜, microenvironments); §6.7 (provenance fields).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

Subtype = Literal["UM", "RB", "OAL"]
Microenvironment = Literal["aqueous", "retina", "orbit"]
KnowledgeGraph = Literal["PrimeKG", "Hetionet", "DRKG"]

SUBTYPES: tuple[Subtype, ...] = ("UM", "RB", "OAL")
KNOWLEDGE_GRAPHS: tuple[KnowledgeGraph, ...] = ("PrimeKG", "Hetionet", "DRKG")

SUBTYPE_MICROENV: dict[Subtype, Microenvironment] = {
    "UM": "aqueous",
    "RB": "retina",
    "OAL": "orbit",
}

MECHANISMS: tuple[str, ...] = (
    "bispecific-TCR",
    "bispecific-TCR+HLA-A*02:01",
    "ICI-PD1-only",
    "PD-L1-blockade",
    "ICI-CTLA4-only",
    "MHC-I-restoration",
    "HLA-E-blockade",
    "NKG2A-antagonism",
    "FasL-neutralisation",
    "TGF-beta-blockade",
    "GD2-CAR-T",
    "CD20-targeted",
    "CD20xCD3-bispecific",
    "adoptive-cell-therapy",
    "oncolytic-HSV",
    "PRAME-TCR",
    "PRAME-ImmTAC",
    "PKC-inhibition",
    "MEK-inhibition",
    "ferroptosis-induction",
    "HDAC-inhibition",
)


@dataclass(frozen=True, slots=True)
class Candidate:
    drug: str
    score: float
    mechanism: str
    paths: int = 1


@dataclass(frozen=True, slots=True)
class ScoredCandidate:
    drug: str
    concordance: float
    tier: int
    mechanism: str
    ci_low: float
    ci_high: float
    high_reliability: bool


class ProvenanceFields(TypedDict):
    query_hash: str
    retrieval_subgraph_hash: str
    kg_edge_ids_touched: list[str]
    mechanism_types_considered: list[str]
    llm_prompt_hash: str
    llm_output_hash: str
    model_version: str
    timestamp: str
    concordance_score: float
    reliability_tier: int
    provenance_coverage_score: float
    schema_version: str
