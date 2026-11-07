"""Sparse mechanism x microenvironment compatibility matrix.

Ref: §6.4 Eq.(3) compat(m, D_microenv); Table 12 compat-entry sweep.

21 mechanisms x 3 subtypes; 47 entries explicit, the remaining pairs default to
1.0 (neutral). The load-bearing entry compat[UM, ICI-PD1-only]=0.2 encodes the
5.6% pooled UM ICI ORR and is never tuned on held-out labels.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ocudrug_graphrag.casework.types import MECHANISMS, SUBTYPES, Subtype

COMPAT_DEFAULT = 1.0

_EXPLICIT: dict[tuple[Subtype, str], float] = {
    ("UM", "bispecific-TCR"): 1.0,
    ("UM", "bispecific-TCR+HLA-A*02:01"): 1.0,
    ("UM", "ICI-PD1-only"): 0.2,
    ("UM", "PD-L1-blockade"): 0.3,
    ("UM", "ICI-CTLA4-only"): 0.3,
    ("UM", "MHC-I-restoration"): 0.9,
    ("UM", "HLA-E-blockade"): 1.0,
    ("UM", "NKG2A-antagonism"): 1.0,
    ("UM", "FasL-neutralisation"): 1.0,
    ("UM", "TGF-beta-blockade"): 0.8,
    ("UM", "PRAME-TCR"): 1.0,
    ("UM", "PRAME-ImmTAC"): 1.0,
    ("UM", "PKC-inhibition"): 0.9,
    ("UM", "MEK-inhibition"): 0.7,
    ("UM", "ferroptosis-induction"): 1.0,
    ("UM", "oncolytic-HSV"): 0.6,
    ("UM", "adoptive-cell-therapy"): 0.9,
    ("RB", "GD2-CAR-T"): 1.0,
    ("RB", "adoptive-cell-therapy"): 1.0,
    ("RB", "bispecific-TCR"): 0.5,
    ("RB", "ICI-PD1-only"): 0.4,
    ("RB", "MHC-I-restoration"): 0.6,
    ("RB", "oncolytic-HSV"): 0.7,
    ("RB", "ferroptosis-induction"): 0.5,
    ("RB", "HDAC-inhibition"): 0.6,
    ("RB", "MEK-inhibition"): 0.5,
    ("RB", "PD-L1-blockade"): 0.4,
    ("RB", "CD20-targeted"): 0.2,
    ("RB", "TGF-beta-blockade"): 0.5,
    ("RB", "HLA-E-blockade"): 0.5,
    ("RB", "NKG2A-antagonism"): 0.5,
    ("RB", "PRAME-TCR"): 0.5,
    ("OAL", "CD20-targeted"): 1.0,
    ("OAL", "CD20xCD3-bispecific"): 1.0,
    ("OAL", "ICI-PD1-only"): 0.5,
    ("OAL", "HDAC-inhibition"): 0.7,
    ("OAL", "bispecific-TCR"): 0.3,
    ("OAL", "GD2-CAR-T"): 0.2,
    ("OAL", "PRAME-TCR"): 0.2,
    ("OAL", "ferroptosis-induction"): 0.4,
    ("OAL", "MHC-I-restoration"): 0.5,
    ("OAL", "adoptive-cell-therapy"): 0.6,
    ("OAL", "MEK-inhibition"): 0.4,
    ("OAL", "PD-L1-blockade"): 0.5,
    ("OAL", "oncolytic-HSV"): 0.3,
    ("OAL", "TGF-beta-blockade"): 0.5,
    ("OAL", "HLA-E-blockade"): 0.4,
}


def explicit_entry_count() -> int:
    return len(_EXPLICIT)


def compat(mechanism: str, subtype: Subtype) -> float:
    return _EXPLICIT.get((subtype, mechanism), COMPAT_DEFAULT)


def compat_matrix() -> NDArray[np.float64]:
    matrix = np.full((len(MECHANISMS), len(SUBTYPES)), COMPAT_DEFAULT, dtype=np.float64)
    for j, subtype in enumerate(SUBTYPES):
        for i, mechanism in enumerate(MECHANISMS):
            matrix[i, j] = compat(mechanism, subtype)
    return matrix
