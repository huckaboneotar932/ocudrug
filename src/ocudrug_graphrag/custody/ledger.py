"""Provenance ledger.

Ref: §6.7; Alg.4. Each prediction emits a schema-validated 12-field record; the
record digest excludes only the wall-clock timestamp so two temperature-0 runs of the
pipeline produce an identical digest (Thm.3 byte-identical re-execution).
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from ocudrug_graphrag.casework.types import ProvenanceFields
from ocudrug_graphrag.custody.canonical import canonicalize, hash_object, sha256_hex

_SCHEMA_PATH = Path(__file__).with_name("schema_v1.0.json")
_FIELD_COUNT = 12


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _is_populated(value: Any) -> bool:
    if isinstance(value, (list, str)):
        return len(value) > 0
    return value is not None


def coverage_score(record: ProvenanceFields) -> float:
    populated = sum(1 for v in record.values() if _is_populated(v))
    return populated / float(_FIELD_COUNT)


def utc_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def build_record(
    *,
    query: str,
    subgraph_fingerprint: str,
    prompt: str,
    output: str,
    edge_ids: list[str],
    mechanisms: list[str],
    model_version: str,
    concordance: float,
    tier: int,
    schema_version: str,
    timestamp: str,
) -> ProvenanceFields:
    record: ProvenanceFields = {
        "query_hash": sha256_hex(query),
        "retrieval_subgraph_hash": subgraph_fingerprint,
        "kg_edge_ids_touched": edge_ids,
        "mechanism_types_considered": mechanisms,
        "llm_prompt_hash": sha256_hex(prompt),
        "llm_output_hash": sha256_hex(output),
        "model_version": model_version,
        "timestamp": timestamp,
        "concordance_score": concordance,
        "reliability_tier": tier,
        "provenance_coverage_score": 0.0,
        "schema_version": schema_version,
    }
    record["provenance_coverage_score"] = coverage_score(record)
    return record


def validate_record(record: ProvenanceFields) -> bool:
    return bool(_validator().is_valid(dict(record)))


def emit_provenance_record(record: ProvenanceFields) -> tuple[ProvenanceFields, bool, float]:
    if not validate_record(record):
        return (record, False, 0.0)
    return (record, True, record["provenance_coverage_score"])


def record_digest(record: ProvenanceFields) -> str:
    payload = {k: v for k, v in record.items() if k != "timestamp"}
    return hash_object(payload)


def append_record(record: ProvenanceFields, ledger_path: Path) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = ledger_path.with_suffix(ledger_path.suffix + ".tmp")
    existing = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
    tmp.write_text(existing + canonicalize(dict(record)) + "\n", encoding="utf-8")
    os.replace(tmp, ledger_path)
