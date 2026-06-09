# Matplotlib Headless Backend

## Status: Completed

## Context

The repository includes a `matplotlibrc` file for notebook presentation
defaults, but the backend selection was still commented out. The checked-in
notebook is source-only and often validated in non-interactive environments,
so the local configuration should prefer the non-GUI Agg backend for historical
reproduction runs.

## Objectives

- Set the checked-in Matplotlib backend to `Agg`.
- Validate the backend choice without executing the notebook or refreshing
  data.
- Document the headless rendering expectation in README and data provenance
  notes.

## Work Completed

- Enabled `backend : Agg` in `matplotlibrc`.
- Extended `scripts/check_notebook_provenance.py` to require the Agg backend.
- Updated README, DATA_PROVENANCE, VISION, and CHANGES notes for the
  headless-backend guard.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `make verify`
- `git diff --check`
