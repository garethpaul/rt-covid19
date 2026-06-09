# Empty Code Cell Guard

## Status: Completed

## Context

The committed notebook is intentionally source-only: execution counts and
outputs are stripped so checked-in artifacts do not imply a fresh data refresh.
Two trailing code cells were empty, which added unfinished placeholder state to
the otherwise source-only notebook.

## Objectives

- Remove empty code cells without executing or refreshing the notebook.
- Keep the notebook JSON valid and source-only.
- Extend static validation to reject future empty code cells.
- Preserve the existing data provenance, dependency, and presentation-default
  checks.

## Work Completed

- Removed two empty trailing code cells from `Rt-covid19.ipynb`.
- Extended `scripts/check_notebook_provenance.py` to reject empty code cells.
- Updated DATA_PROVENANCE, README, VISION, and CHANGES notes for the guard.
- Added this completed plan under `docs/plans/`.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `make verify`
- `git diff --check`
