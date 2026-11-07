"""Command-line entry points; data and model integration is required."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast, get_args

from clize import run

from ocudrug_graphrag.casework.config import PipelineConfig, load_config
from ocudrug_graphrag.casework.types import SUBTYPES, Subtype
from ocudrug_graphrag.custody import append_record, record_digest
from ocudrug_graphrag.proceedings import run_pipeline


def _config(config: str) -> PipelineConfig:
    return load_config(config) if config else PipelineConfig()


def _subtype(value: str) -> Subtype:
    if value not in get_args(Subtype):
        raise ValueError(f"subtype must be one of {SUBTYPES}, got {value!r}")
    return cast(Subtype, value)


def build(subtype: str, *, config: str = "", seed: int = 42) -> None:
    """Build subgraphs after a source loader is integrated.

    :param subtype: one of UM, RB, OAL
    :param config: path to a TOML experiment config
    :param seed: random seed
    """
    raise NotImplementedError("Knowledge graph loading requires a source-specific parser.")


def rank(subtype: str, *, config: str = "", seed: int = 42, top: int = 20) -> None:
    """Rank candidates after the pipeline is integrated.

    :param subtype: one of UM, RB, OAL
    :param config: path to a TOML experiment config
    :param seed: random seed
    :param top: number of candidates to print
    """
    st = _subtype(subtype)
    result = run_pipeline(st, _config(config), seed=seed)
    for i, pred in enumerate(result.predictions[:top], start=1):
        c = pred.candidate
        flag = "HIGH" if c.high_reliability else "single-KG"
        print(
            f"{i:2d}. {c.drug:28s} tier={c.tier} conc={c.concordance:.3f} "
            f"[{c.ci_low:.3f},{c.ci_high:.3f}] {flag:9s} {c.mechanism}"
        )


def evaluate(*, config: str = "") -> None:
    """Evaluate results after data and reference labels are integrated.

    :param config: path to a TOML experiment config
    """
    raise NotImplementedError("Evaluation requires source data and reference labels.")


def audit(subtype: str, *, config: str = "", seed: int = 42) -> None:
    """Audit results after the pipeline is integrated.

    :param subtype: one of UM, RB, OAL
    :param config: path to a TOML experiment config
    :param seed: random seed
    """
    st = _subtype(subtype)
    cfg = _config(config)
    first = [record_digest(p.provenance) for p in run_pipeline(st, cfg, seed=seed).predictions]
    second = [record_digest(p.provenance) for p in run_pipeline(st, cfg, seed=seed).predictions]
    ok = first == second
    print(f"audited {len(first)} records; byte-identical re-execution: {ok}")


def export(out: str, *, config: str = "", subtype: str = "UM", seed: int = 42) -> None:
    """Export results after the pipeline is integrated.

    :param out: output directory
    :param config: path to a TOML experiment config
    :param subtype: one of UM, RB, OAL
    :param seed: random seed
    """
    st = _subtype(subtype)
    result = run_pipeline(st, _config(config), seed=seed)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    ledger = out_dir / f"{st}.ledger.jsonl"
    if ledger.exists():
        ledger.unlink()
    ranking = []
    for pred in result.predictions:
        append_record(pred.provenance, ledger)
        ranking.append(
            {
                "drug": pred.candidate.drug,
                "tier": pred.candidate.tier,
                "concordance": pred.candidate.concordance,
            }
        )
    (out_dir / f"{st}.ranking.json").write_text(json.dumps(ranking, indent=2), encoding="utf-8")
    print(f"wrote {len(ranking)} records to {out_dir}")


def main() -> None:
    run(build, rank, evaluate, audit, export)


if __name__ == "__main__":
    main()
