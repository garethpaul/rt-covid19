# Pandas Squeeze Constraint

## Status: Completed

## Context

The notebook still uses `pandas.read_csv(..., squeeze=True)`, a legacy pandas
behavior that is not compatible with pandas 2. The repository already declared
`pandas<2` in `requirements.txt`, but the provenance checker only verified that
pandas was listed at all.

## Objectives

- Preserve the historical notebook source without refreshing data or outputs.
- Keep the pandas upper bound tied to the notebook's current source.
- Require README and data provenance notes to explain the compatibility
  constraint.
- Avoid broader dependency modernization in this focused pass.

## Work Completed

- Extended `scripts/check_notebook_provenance.py` to detect
  `squeeze=True` usage and require `pandas<2`.
- Required README and `DATA_PROVENANCE.md` to document the pandas compatibility
  constraint.
- Updated README, DATA_PROVENANCE, VISION, and CHANGES notes for the guard.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `git diff --check`
