"""Pipeline result types and integration boundary."""
from __future__ import annotations

from dataclasses import dataclass

from ocudrug_graphrag.casework.config import PipelineConfig
from ocudrug_graphrag.casework.types import ProvenanceFields, ScoredCandidate, Subtype
from ocudrug_graphrag.deposition import Narration


@dataclass(frozen=True, slots=True)
class PredictionRecord:
    candidate: ScoredCandidate
    narration: Narration
    provenance: ProvenanceFields


@dataclass(frozen=True, slots=True)
class RankedResult:
    subtype: Subtype
    predictions: list[PredictionRecord]

    def ranking(self) -> list[str]:
        return [p.candidate.drug for p in self.predictions]


def run_pipeline(subtype: Subtype, config: PipelineConfig, *, seed: int = 42) -> RankedResult:
    raise NotImplementedError(
        "The pipeline requires integration with knowledge graphs, a trained path scorer, "
        "independent interval estimates, narration providers, and path-level provenance."
    )
