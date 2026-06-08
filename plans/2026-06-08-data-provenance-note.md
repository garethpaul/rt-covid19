# Data Provenance Note

## Status

Completed

## Context

The notebook and README identify the NYT county COVID-19 data URL, but the
repository needs a durable provenance note that explains runtime download
behavior, preprocessing, refresh status, and interpretation caveats.

## Objectives

- Add `DATA_PROVENANCE.md` for the notebook data source and preprocessing
  assumptions.
- Clarify that no dataset refresh was performed during this maintenance pass.
- Link provenance from README.
- Extend `scripts/check_notebook_provenance.py` so the data-source URL,
  refresh status, and public-health caveat remain documented.

## Verification

- `make lint`
- `make verify`
- `git diff --check`
