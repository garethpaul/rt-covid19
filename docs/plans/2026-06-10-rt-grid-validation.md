# Rt Grid Validation

## Status: Completed

## Context

`get_posteriors` accepted any finite one-dimensional custom Rt grid. Negative
or duplicate values violate the model domain and ordered transition-grid
assumption, allowing invalid priors or duplicate posterior indices to reach
later calculations.

## Objectives

- Reject negative custom Rt values.
- Reject duplicate or descending custom Rt grid points.
- Preserve the default grid and valid custom-grid calculations.

## Work Completed

- Added a non-negative, strictly increasing custom-grid validation guard.
- Added regression coverage for negative and duplicate grid values.
- Updated README, SECURITY, VISION, and CHANGES model guidance.

## Verification

- `python3 -m unittest discover -s tests -p "test*.py"`
- `make check`
- `make verify`
- `git diff --check`
