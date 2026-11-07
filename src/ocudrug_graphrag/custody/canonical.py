"""Canonical JSON serialisation for hashing.

Ref: §6.7 (RFC 8785 canonicalisation followed by SHA-256). Object keys are sorted,
whitespace removed, and floats fixed to a stable precision so the octet sequence is
reproducible across runs.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

_FLOAT_DECIMALS = 6


def _normalise(obj: Any) -> Any:
    if isinstance(obj, float):
        return round(obj, _FLOAT_DECIMALS)
    if isinstance(obj, dict):
        return {str(k): _normalise(v) for k, v in sorted(obj.items())}
    if isinstance(obj, (list, tuple)):
        return [_normalise(v) for v in obj]
    return obj


def canonicalize(obj: Any) -> str:
    return json.dumps(
        _normalise(obj),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_hex(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def hash_object(obj: Any) -> str:
    return sha256_hex(canonicalize(obj))
