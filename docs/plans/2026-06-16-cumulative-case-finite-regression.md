---
title: Cumulative Case Finite Regression
status: completed
date: 2026-06-16
---

# Cumulative Case Finite Regression

## Status: Completed

## Priority

P1 model correctness. `prepare_cases()` rejects non-finite cumulative values,
but the guard has no focused regression or mutation-sensitive provenance
contract and can be removed without the current suite detecting the change.

## Approach

- Add focused `NaN`, positive-infinity, and negative-infinity regressions.
- Require the finite-value guard to remain after numeric conversion and before
  differencing.
- Keep runtime model behavior, smoothing, revision handling, dependencies, and
  notebook outputs unchanged.

## Verification

- Demonstrate that deleting the finite-value guard is rejected by the focused
  test and provenance contract.
- Run the focused test, complete synthetic model suite, Ruff, notebook JSON,
  `pip check`, and `pip-audit` in the pinned isolated Python 3.12 environment.
- Run `make check` from the repository and through the absolute Makefile path
  from an external directory.
- Audit exact paths, generated caches, secrets, conflict markers, binaries,
  large files, and whitespace.

## Scope Boundaries

- Do not change preprocessing output for finite cumulative inputs.
- Do not change smoothing parameters, Rt likelihoods, HDI behavior, dataset
  fingerprints, dependency pins, notebook outputs, or workflow shape.
- Do not fetch live public-health data or present current health guidance.
- Keep PR #10 and its predecessors open and preserve base-first stack ordering.

## Work Completed

- Added focused regressions for `NaN`, positive infinity, and negative infinity
  at the cumulative-case preprocessing boundary.
- Extended notebook-independent provenance checks to keep the finite guard
  ordered after numeric conversion and before negative-value validation and
  differencing.
- Updated README, provenance, security, vision, and changelog guidance with the
  finite cumulative cases invariant.

## Verification Completed

- The focused non-finite cumulative-value tests passed, and the complete
  30-test synthetic model suite passed.
- Ruff format and lint checks, notebook JSON validation, `pip check`, and
  `pip-audit` passed in a clean pinned Python 3.12 environment with
  `PYTHONPATH` removed.
- The isolated `make check` passed from the repository and through the absolute
  Makefile path from an external directory.
- Seven hostile finite-value mutations were rejected across implementation,
  regression, checker, documentation, and completed-plan contracts.
- Exact diff, whitespace, generated-artifact, conflict-marker, file-mode,
  binary, large-file, and credential-shaped-addition audits passed.
