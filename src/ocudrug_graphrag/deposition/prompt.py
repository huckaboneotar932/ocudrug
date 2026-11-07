"""Stage 4 prompt construction.

Ref: Alg.3 line 2; §6.6 (strict "describe the path; do not propose" framing). The
prompt includes the retrieved mechanism, concordance and tier. Outputs require verification.
"""

from __future__ import annotations

from ocudrug_graphrag.casework.types import Subtype


def construct_prompt(
    drug: str, subtype: Subtype, mechanism: str, concordance: float, tier: int
) -> str:
    return (
        f"Describe the retrieved evidence for {drug} in {subtype}. "
        f"Mechanism={mechanism}; concordance={concordance:.3f}; reliability_tier={tier}. "
        "Describe the path only; do not propose a new mechanism."
    )
