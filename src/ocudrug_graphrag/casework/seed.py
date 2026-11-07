"""Deterministic seeding.

Ref: §6.5 (numpy.random.PCG64); Table 8 (seeds {42,123,256,389,512}).
"""

from __future__ import annotations

import hashlib
import random

import numpy as np

DEFAULT_SEEDS: tuple[int, ...] = (42, 123, 256, 389, 512)


def set_seed(seed: int) -> np.random.Generator:
    random.seed(seed)
    np.random.seed(seed % (2**32))
    return np.random.Generator(np.random.PCG64(seed))


def stable_seed(*parts: str | int) -> int:
    payload = "|".join(str(p) for p in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def stable_rng(*parts: str | int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(stable_seed(*parts)))
