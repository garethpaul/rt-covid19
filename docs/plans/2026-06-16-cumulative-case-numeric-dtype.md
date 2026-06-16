---
title: Cumulative Case Numeric Dtype Validation
status: planned
date: 2026-06-16
---

# Cumulative Case Numeric Dtype Validation

## Priority

P1 model correctness. `prepare_cases()` currently accepts boolean and complex
cumulative case Series; booleans are treated as counts and complex values lose
their imaginary components during smoothing.

## Problem

The cumulative-case entry point checks only `is_numeric_dtype()`. Pandas treats
boolean and complex dtypes as numeric, while the downstream posterior entry
point already rejects both. The inconsistent boundary allows invalid source
data to be normalized into plausible-looking daily cases.

## Approach

- Require cumulative cases to use a real numeric, non-boolean dtype before
  differencing or smoothing.
- Preserve the existing non-empty Series, index, finite-value, and alignment
  contracts.
- Add focused boolean and complex regressions plus ordinary integer and float
  acceptance coverage.
- Extend notebook-independent static contracts, maintenance guidance,
  changelog, and completed verification evidence.

## Files

- `rt_covid19.py`
- `tests/test_rt_covid19.py`
- `scripts/check_notebook_provenance.py`
- `README.md`
- `DATA_PROVENANCE.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-cumulative-case-numeric-dtype.md`

## Verification

- Preserve the pre-fix evidence that boolean and complex cumulative cases are
  accepted and complex values emit lossy-cast warnings.
- Run focused dtype tests and the complete synthetic model suite.
- Run Ruff format/lint, notebook provenance and JSON checks, `pip check`,
  `pip-audit`, repository `make check`, and the absolute-Makefile gate from an
  external directory in an isolated Python 3.12 environment.
- Reject isolated implementation, test, checker, guidance, changelog, and
  completed-plan mutations.
- Audit exact paths, generated caches, secrets, conflict markers, binaries,
  large files, and whitespace.

## Scope Boundaries

- Do not change smoothing parameters, Rt likelihoods, HDI behavior, dataset
  fingerprints, notebook outputs, dependency pins, or workflow shape.
- Do not fetch the live COVID-19 dataset or present current health guidance.
- Keep PR #8 and its predecessors open and retain base-first stack ordering.

## Success Criteria

- Boolean and complex cumulative case Series fail before differencing or
  smoothing.
- Integer and floating-point Series retain existing behavior.
- Cumulative and smoothed case entry points enforce consistent dtype semantics.

## Verification Completed

Pending implementation and bounded verification.
