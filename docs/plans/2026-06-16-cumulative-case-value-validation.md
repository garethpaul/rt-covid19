---
title: Cumulative Case Value Validation
status: completed
date: 2026-06-16
---

# Cumulative Case Value Validation

## Status: Completed

## Priority

P1 model correctness. `prepare_cases()` accepts negative cumulative case totals
and can transform an entirely invalid negative series into plausible positive
daily and smoothed values.

## Problem

The cumulative-case boundary requires a non-empty, indexed, real numeric,
finite Series but does not require non-negative totals. Because differencing
depends on relative changes, steadily increasing negative totals can pass every
downstream check and produce credible-looking model inputs.

## Approach

- Reject any negative cumulative case total before differencing or smoothing.
- Preserve finite zero and positive integer or floating-point inputs.
- Do not reject downward revisions solely because a cumulative series is not
  monotonic; historical reporting corrections remain outside this narrow fix.
- Add focused regressions, mutation-sensitive static contracts, maintenance
  guidance, changelog, and completed verification evidence.

## Files

- `rt_covid19.py`
- `tests/test_rt_covid19.py`
- `scripts/check_notebook_provenance.py`
- `README.md`
- `DATA_PROVENANCE.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-cumulative-case-value-validation.md`

## Verification

- Preserve the pre-fix evidence that negative cumulative totals are accepted
  and normalized into plausible daily values.
- Run focused cumulative-value tests and the complete synthetic model suite.
- Run Ruff format/lint, notebook provenance and JSON checks, `pip check`,
  `pip-audit`, repository `make check`, and the absolute-Makefile gate from an
  external directory in the existing isolated Python 3.12 environment.
- Reject isolated implementation, test, checker, guidance, changelog, and
  completed-plan mutations.
- Audit exact paths, generated caches, secrets, conflict markers, binaries,
  large files, and whitespace.

## Scope Boundaries

- Do not change smoothing parameters, revision handling, Rt likelihoods, HDI
  behavior, dataset fingerprints, notebook outputs, dependency pins, or
  workflow shape.
- Do not fetch the live COVID-19 dataset or present current health guidance.
- Keep PR #9 and its predecessors open and retain base-first stack ordering.

## Success Criteria

- Any negative cumulative case value fails before differencing or smoothing.
- Zero and positive integer or floating-point Series retain existing behavior.
- Static and maintainer contracts keep the value boundary visible.

## Work Completed

- Added a non-negative cumulative-value guard before differencing and Gaussian
  smoothing.
- Added focused all-negative and mixed-negative regressions while retaining
  zero and positive integer and floating-point coverage.
- Extended notebook-independent static contracts, provenance, security,
  maintenance guidance, changelog, and plan indexing.

## Verification Completed

- Pre-fix evidence confirmed that negative cumulative totals were accepted and
  normalized into plausible positive daily and smoothed values.
- The focused cumulative-value tests passed, and the complete 29-test synthetic
  model suite passed.
- Ruff format and lint checks, notebook JSON validation, `pip check`, and
  `pip-audit` passed in an isolated pinned Python 3.12 environment.
- The isolated `make check` passed from the repository and through the absolute
  Makefile path from an external directory.
- Seven hostile cumulative-value mutations were rejected across the
  implementation, regressions, static checker, guidance, changelog, and
  completed plan.
- Exact diff, whitespace, generated-artifact, conflict-marker, file-mode,
  binary, large-file, and credential-shaped-addition audits passed.
