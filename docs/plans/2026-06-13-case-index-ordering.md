# Case Index Ordering Contract

## Status: Completed

## Context

`prepare_cases` and `get_posteriors` validate case values but assume their
Series indexes identify one ordered observation per day. Duplicate labels can
make posterior column lookup return multiple columns, descending labels reverse
the modeled timeline, and missing or MultiIndex labels make output alignment
ambiguous.

## Priority

Rt calculations are order-sensitive. The reusable model helpers should reject
ambiguous observation axes before rolling, likelihood, or matrix operations so
offline callers receive a deterministic error rather than misleading output or
downstream pandas shape failures.

## Objectives

- Require one-dimensional Series indexes.
- Reject missing labels, duplicate labels, and descending/unordered labels.
- Apply the same contract to preprocessing and posterior calculation.
- Preserve increasing integer and DatetimeIndex callers.
- Add focused offline regression and hostile mutation coverage.
- Keep the historical notebook, dataset snapshot, and numerical formulas
  unchanged.

## Work Completed

- Added a shared observation-index validator for model Series inputs.
- Required one-dimensional, non-missing, unique, monotonic increasing labels.
- Applied the same validator before preprocessing and posterior calculations.
- Added shared invalid fixtures for duplicate, descending, missing, and
  MultiIndex labels while retaining valid integer and DatetimeIndex coverage.
- Added fail-closed source, test, documentation, and plan contracts.
- Updated README, security, vision, change, and data-provenance documentation.

## Verification

- Focused unit tests for valid and invalid indexes
- Fresh Python 3.12 `make check`
- Read-only network-isolated Python 3.12.8 `make verify`
- Focused missing, duplicate, descending, MultiIndex, bypass, and test-wiring
  mutations
- Notebook JSON, Python syntax, secret, bytecode, and `git diff --check` audits

The offline suite passed 17 tests. Ruff 0.15.16, the provenance checker,
notebook JSON validation, and the read-only network-isolated Python 3.12.8
`make verify` gate passed with exact pinned dependencies.

## Scope Boundary

This change validates observation ordering only. It does not reinterpret
negative daily revisions, execute the live notebook, or alter Rt/HDI formulas.
