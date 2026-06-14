# HDI DataFrame Column Integrity

## Status: In Progress

## Context

`highest_density_interval` recursively processes each posterior `DataFrame`
column. An empty frame currently returns an empty result, while duplicate
column labels make `pmf[column]` return another `DataFrame` and recurse until
Python raises `RecursionError`.

## Priority

High correctness and reliability. Ambiguous observation labels must fail at
the public model boundary rather than trigger unbounded recursion or silently
produce no intervals.

## Requirements

- Reject posterior DataFrames with no columns or no rows.
- Require one-dimensional, non-missing, unique column labels.
- Validate the complete DataFrame shape before per-column recursion.
- Preserve valid column order and existing Series HDI behavior.
- Raise a stable `ValueError` for invalid observation columns.
- Add behavior and static mutation-sensitive coverage.

## Scope Boundaries

- Do not change PMF normalization, probability validation, grid validation,
  interval-width selection, endpoint labels, notebook output, or data loading.

## Verification

- focused empty, duplicate, missing, and MultiIndex column tests
- full isolated `make check` and external-directory gate
- hostile validation, recursion-bypass, test, and completed-plan mutations
- exact diff, generated-artifact, bytecode, and credential-pattern audits
