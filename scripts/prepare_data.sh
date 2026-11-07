#!/usr/bin/env bash
set -euo pipefail

# The public sources below are access-controlled or large; download them into
# data/ and implement source-specific parsing in intake/loaders.py.

cat <<'SOURCES'
PrimeKG v2023       https://doi.org/10.7910/DVN/IXA7BM     (MIT + CC0)
Hetionet v1.0       https://het.io                          (CC0 1.0)
DRKG 2026-04        https://github.com/gnn4dr/DRKG          (Apache 2.0)
TCGA-UVM            https://portal.gdc.cancer.gov/projects/TCGA-UVM (NIH open)
DepMap UM 24Q4      https://depmap.org/portal               (CC-BY-4.0)
cBioPortal UM       https://www.cbioportal.org              (open-use)
ClinicalTrials.gov  https://clinicaltrials.gov              (public, v2 API)
DGIdb v5.0          https://www.dgidb.org                   (open)
OncoKB              https://www.oncokb.org                  (academic)
ChEMBL v34          https://www.ebi.ac.uk/chembl            (CC-BY-SA 3.0)
PubMed / bioRxiv    https://pubmed.ncbi.nlm.nih.gov         (public / CC-BY)
MONDO (root anchor) https://mondo.monarchinitiative.org     (CC0)
SOURCES
