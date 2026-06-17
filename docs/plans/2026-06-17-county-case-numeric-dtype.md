---
title: County Case Numeric Dtype
status: in-progress
date: 2026-06-17
---

# County Case Numeric Dtype

## Status: In Progress

## Priority

P1 data integrity. `load_counties()` accepts any pandas numeric dtype, and pandas
classifies booleans as numeric. A local CSV containing `False` and `True` case
totals therefore passes ingestion and exposes booleans as cumulative counts,
despite downstream model boundaries requiring real numeric, non-boolean data.

## Requirements

- Reject boolean county case totals at the ingestion boundary.
- Reject complex county case totals when a caller-provided reader returns them.
- Continue accepting ordinary integer and floating case totals.
- Preserve finite, non-negative, sorting, remote URL, size, digest, timeout, and
  download-limit behavior.
- Keep the reviewed data snapshot, dependency pins, workflow, notebook, and
  public API unchanged.

## Approach

- Align `load_counties()` with the existing explicit real numeric, non-boolean
  dtype checks used by cumulative preprocessing and posterior calculation.
- Validate dtype before float coercion, finite checks, and value checks so
  booleans and complex values cannot pass through lossy conversion.
- Add focused invalid and valid dtype fixtures plus mutation-sensitive
  provenance and completed-plan contracts.

## Scope Boundaries

- Do not fetch live public-health data or change the pinned NYT snapshot.
- Do not alter cumulative differencing, smoothing, Rt likelihoods, HDIs,
  notebook outputs, dependencies, or workflow shape.
- Keep PR #11 and its predecessors open and preserve base-first stack ordering.

## Implementation Units

- `rt_covid19.py`: enforce the county case dtype boundary before conversion.
- `tests/test_rt_covid19.py`: cover boolean and complex rejection plus integer
  and floating acceptance.
- `scripts/check_notebook_provenance.py`: protect implementation ordering,
  focused regression registration, documentation, and completed evidence.
- `README.md`, `DATA_PROVENANCE.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`:
  document the ingestion dtype invariant.

## Verification

- Run the focused tests and complete pinned `make check` from the repository
  and through the absolute Makefile path from an external directory.
- Reject hostile mutations that remove numeric, boolean, or complex guards;
  bypass focused tests; weaken guidance; or falsify completed evidence.
- Audit exact paths, generated caches, secrets, conflict markers, modes,
  binaries, large files, dependency/workflow drift, and upstream equality.

## Risks

- Pandas treats booleans as numeric, so a generic numeric check is insufficient.
- Complex values must be rejected before float conversion rather than relying
  on conversion warnings or truncation.
