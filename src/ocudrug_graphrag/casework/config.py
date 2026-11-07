"""Pipeline configuration loaded from TOML and validated with Pydantic.

Ref: Table 8 (Supplementary S3) hyperparameters; Table 12 operating point.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class DistillConfig(BaseModel):
    depth_h: int = 2
    degree_cap: int = 64
    sparse_expand_k: int = 3
    subgraph_min: int = 5000
    subgraph_max: int = 10000


class WorkupConfig(BaseModel):
    hidden_dim: int = 64
    path_cap_l: int = 3
    top_m: int = 50
    compat_default: float = 1.0


class ConcordanceConfig(BaseModel):
    alpha: float = 0.6
    top_k: int = 20
    bootstrap_b: int = 200
    tier2_min: int = 2
    tier3_min: int = 3


class DepositionConfig(BaseModel):
    temperature: float = 0.0
    verifier_enabled: bool = False
    verifier_theta: float = 0.80
    max_refine: int = 2
    primary_model: str = ""
    crosscheck_model: str = ""
    replicate_model: str = ""


class ProvenanceConfig(BaseModel):
    coverage_target: float = 0.80
    schema_version: str = "schema_v1.0.json"
    hash_algorithm: str = "SHA-256"


class PipelineConfig(BaseModel):
    name: str = "main"
    beta: float = 0.0
    seeds: list[int] = Field(default_factory=lambda: [42, 123, 256, 389, 512])
    distill: DistillConfig = Field(default_factory=DistillConfig)
    workup: WorkupConfig = Field(default_factory=WorkupConfig)
    concordance: ConcordanceConfig = Field(default_factory=ConcordanceConfig)
    deposition: DepositionConfig = Field(default_factory=DepositionConfig)
    provenance: ProvenanceConfig = Field(default_factory=ProvenanceConfig)


def load_config(path: str | Path) -> PipelineConfig:
    raw = Path(path).read_bytes()
    data = tomllib.loads(raw.decode("utf-8"))
    return PipelineConfig.model_validate(data)
