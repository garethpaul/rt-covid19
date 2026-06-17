---
title: State-Qualified County Identity
status: in_progress
date: 2026-06-17
---

# State-Qualified County Identity

## Status: In Progress

## Priority

P1 data integrity. The pinned NYT county dataset contains counties with the same
name in different states, but `_read_counties()` currently discards `state` and
indexes observations only by county and date. Notebook selection and batch
grouping can therefore merge distinct counties into one cumulative case series.
For example, the reviewed snapshot contains Douglas County observations for
Colorado and Nebraska on the same date with different totals.

## Requirements

- Retain `state` while parsing county data and expose a unique, non-missing
  `(state, county, date)` index in that order.
- Reject reader results that do not provide the exact state-qualified index
  contract before case values reach model preprocessing.
- Select the notebook's Marin example explicitly as Marin, California.
- Limit the notebook batch example to its intended California counties and
  group each time series by both state and county.
- Add a regression proving same-name counties in different states remain
  separate series with their original values.
- Preserve the pinned dataset snapshot, formulas, dependency pins, workflows,
  existing numeric/value guards, and source-only notebook outputs.

## Approach

- Parse the `state` column alongside date, county, and cases, using a
  state/county/date `MultiIndex`.
- Validate the exact index names, missing labels, and uniqueness in
  `load_counties()` before dtype conversion and value validation.
- Update notebook selection to use a state/county tuple and reduce the selected
  result to its date index before calling `prepare_cases()`.
- Filter the batch example to California first, group by state and county, and
  reduce each grouped series to a date index while keeping human-readable
  county labels for the existing result and plot flow.
- Extend the provenance checker so source, notebook usage, regression coverage,
  documentation, and completed verification evidence are mutation-sensitive.

## Scope Boundaries

- Do not refresh or otherwise alter the immutable NYT data snapshot.
- Do not broaden the notebook's existing Bay Area and Sacramento-area target
  list or change its statistical calculations.
- Do not introduce FIPS-based identity, geospatial normalization, or a general
  location abstraction in this change.
- Keep PR #12 and its predecessors open and preserve base-first stack ordering.

## Implementation Units

- `rt_covid19.py`: retain state and enforce the state/county/date index schema.
- `Rt-covid19.ipynb`: qualify single-county and batch selections by state.
- `tests/test_rt_covid19.py`: cover exact schema rejection and same-name county
  separation without weakening existing loader tests.
- `scripts/check_notebook_provenance.py`: protect implementation order,
  notebook selection/grouping, focused regressions, guidance, and plan evidence.
- `README.md`, `DATA_PROVENANCE.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`:
  document state-qualified county identity and its data-integrity consequence.

## Verification

- Run focused loader and provenance tests, then the complete pinned `make check`
  from the repository and through the absolute Makefile path externally.
- Reject hostile mutations that drop state parsing, weaken index validation,
  restore county-only notebook selection/grouping, bypass regressions, or
  falsify completed plan evidence.
- Audit exact paths, notebook outputs, generated caches, credentials, conflict
  markers, modes, binaries, large files, dependency/workflow drift, and
  upstream equality before committing.

## Risks

- Existing mocked loader tests may accidentally rely on one-level indexes; test
  fixtures must express the production schema rather than bypassing it.
- Grouped notebook series retain grouping levels by default; those levels must
  be removed before the existing one-dimensional date-index model boundary.
- County names remain presentation labels only after filtering to one state;
  the data identity itself must stay state-qualified through selection.

## Work Completed

- Pending implementation.

## Verification Completed

- Pending implementation and validation.
