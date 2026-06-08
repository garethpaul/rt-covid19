# Strip Notebook Outputs

## Status: Completed

## Context

`Rt-covid19.ipynb` is a historical public-health analysis notebook that reads
external data at runtime. Stored output cells and execution counts can make the
checked-in notebook look like a current data refresh even when no refresh was
performed.

## Objectives

- Preserve the notebook source, markdown narrative, formulas, and code cells.
- Remove stale execution outputs and execution counts from the committed
  notebook.
- Extend provenance checks so future commits keep the notebook source-only.
- Document the source-only notebook policy alongside the data provenance notes.

## Work Completed

- Cleared all code-cell `outputs` and `execution_count` fields from
  `Rt-covid19.ipynb`.
- Updated the notebook provenance checker to reject stored outputs and
  execution counts.
- Updated README, DATA_PROVENANCE, VISION, and CHANGES.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add an execution environment lockfile if the notebook is intentionally
  refreshed.
- Move reusable Rt calculations into importable Python modules with unit tests.
