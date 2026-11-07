"""Narration using caller-provided model and agreement interfaces."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ocudrug_graphrag.casework.config import DepositionConfig
from ocudrug_graphrag.casework.types import ScoredCandidate, Subtype
from ocudrug_graphrag.deposition.prompt import construct_prompt

Narrator = Callable[[str, str], str]
Agreement = Callable[[str, str], float]


@dataclass(frozen=True, slots=True)
class Narration:
    drug: str
    prompt: str
    primary: str
    crosscheck: str
    replicate: str
    agreement: float
    refinements: int


def narrate_candidate(
    candidate: ScoredCandidate,
    subtype: Subtype,
    config: DepositionConfig,
    *,
    narrator: Narrator,
    agreement_fn: Agreement,
) -> Narration:
    if not all((config.primary_model, config.crosscheck_model, config.replicate_model)):
        raise ValueError("Model identifiers must be supplied for narration.")
    prompt = construct_prompt(
        candidate.drug, subtype, candidate.mechanism, candidate.concordance, candidate.tier
    )
    primary = narrator(config.primary_model, prompt)
    cross = narrator(config.crosscheck_model, prompt)
    agreement = agreement_fn(primary, cross)
    refinements = 0
    if config.verifier_enabled:
        while agreement < config.verifier_theta and refinements < config.max_refine:
            cross = narrator(config.crosscheck_model, prompt)
            agreement = agreement_fn(primary, cross)
            refinements += 1
    replicate = narrator(config.replicate_model, prompt)
    return Narration(candidate.drug, prompt, primary, cross, replicate, agreement, refinements)
