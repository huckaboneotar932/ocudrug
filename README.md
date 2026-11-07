# OcuDrug-GraphRAG

OcuDrug-GraphRAG provides components for knowledge-graph retrieval, candidate concordance and provenance in ocular oncology research.

## Installation

```bash
python -m pip install -e ".[dev]"
```

## Data and execution

Knowledge graph dumps, reference labels, trained path-scoring weights and model services are not included. `scripts/prepare_data.sh` lists source providers; `intake/loaders.py` requires source-specific parsing before it can load records.

`intake.OcularSubgraph` and `distill_subgraph` accept graphs supplied by the caller. `workup.retrieve_paths` requires a caller-provided path scorer. `deposition.narrate_candidate` requires actual narration and agreement providers and configured model identifiers.

The end-to-end pipeline and command-line ranking, evaluation, auditing and export require integration with the data sources, scorer, independent interval estimates, narration providers and path-level provenance before use. They currently stop with an error rather than emit unsupported results. The project has not been validated for clinical use.

## Modules

`intake` contains graph structures and distillation; `workup` contains retrieval and scoring utilities; `concordance` provides agreement calculations; `deposition` defines narration interfaces; `custody` handles provenance records; `register` contains evaluation metrics.

```bash
pytest -q
```
