# Highest Density Interval Grid Validation

## Status: Completed

## Context

`highest_density_interval` validates probability mass but returns labels from
the supplied Series index without validating that the index is a numeric,
finite, strictly increasing grid. Duplicate, unsorted, non-numeric, or
non-finite labels can therefore produce interval endpoints that do not describe
an ordered Rt range.

## Priority

The helper is part of the tested model API and feeds notebook summary tables.
Its interval endpoints should only be derived from a well-defined numeric grid.

## Requirements

- R1. Preserve Series and DataFrame HDI behavior for valid ordered grids.
- R2. Require a one-dimensional numeric index with one label per PMF value.
- R3. Reject non-finite, duplicate, non-increasing, or non-numeric labels with
  a clear `ValueError`.
- R4. Preserve existing PMF mass and probability validation.
- R5. Cover valid and hostile grid cases in the offline unit suite.
- R6. Protect implementation, tests, docs, and completed plan in the notebook
  provenance checker.

## Scope Boundaries

- Do not change the HDI search algorithm or tie-breaking behavior.
- Do not refresh historical COVID-19 data or notebook outputs.
- Do not change dependency versions.

## Verification Plan

- `python3 -m unittest discover -s tests -p "test*.py"`
- `make lint`
- `make test`
- `make check`
- focused hostile HDI-grid mutations
- `git diff --check`

## Work Completed

- Added explicit one-dimensional, numeric, non-boolean HDI index validation.
- Required finite, strictly increasing labels before interval endpoints are
  selected while preserving the original validated index labels.
- Added offline coverage for duplicate, unsorted, non-finite, string, boolean,
  and multi-level indexes while preserving Series and DataFrame behavior.
- Extended the provenance checker and README, VISION, CHANGES, and data
  provenance guidance with the completed boundary.

## Verification

- `python3 -m unittest discover -s tests -p "test*.py"` passed 12 tests.
- `make lint`, `make test`, and `make verify` passed.
- `make check` passed in a fresh Python 3.12 virtual environment with the
  pinned runtime and development requirements.
- The host-wide `make dependencies` command was not used as release evidence
  because the shell's broad `PYTHONPATH` injects unrelated internal packages
  and the global environment also has a `virtualenv`/`platformdirs` conflict;
  the isolated environment cleared `PYTHONPATH` and had no conflicts.
- 12 focused hostile HDI-grid mutations were rejected, covering dimensional,
  type, boolean, finite, ordering, validation-bypass, error, test,
  documentation, and completed-plan guards.
- `git diff --check` passed.
