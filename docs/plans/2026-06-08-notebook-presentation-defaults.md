# Notebook Presentation Defaults

## Status: Completed

## Context

`Rt-covid19.ipynb` is kept source-only and is usually validated without
executing a data refresh. Later summary plotting cells referenced presentation
symbols such as `FILTERED_REGIONS`, status groups, and color constants, but the
notebook did not define them. That made a fresh notebook run depend on missing
state from an older interactive session.

## Objectives

- Keep default verification dependency-free and non-refreshing.
- Define neutral presentation defaults in the notebook source.
- Validate that summary-plot defaults remain defined before future notebook
  edits.
- Preserve existing provenance, dependency, output-stripping, and completed-plan
  checks.

## Work Completed

- Added neutral filtered-region, status-group, and color defaults to the
  notebook import/setup cell.
- Extended `scripts/check_notebook_provenance.py` to require those assignments.
- Documented that the defaults are presentation inputs, not current
  public-health policy.
- Updated README, VISION, and CHANGES notes for the new guardrail.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `make verify`
- `git diff --check`
