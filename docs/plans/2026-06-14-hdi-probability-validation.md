# HDI Probability Validation

## Status: Completed

## Context

`highest_density_interval` compares `p` directly with numeric bounds. Invalid
types such as `None` and strings therefore leak comparison `TypeError` instead
of the model helper's stable `ValueError` boundary.

## Requirements

- Accept finite real numeric probabilities strictly between zero and one.
- Reject booleans, non-numeric values, complex values, NaN, infinities, and
  inclusive endpoints with one stable `ValueError` message.
- Accept in-range built-in and NumPy floating scalars while applying the same
  open-interval rejection to integer endpoints.
- Preserve Series/DataFrame validation, normalization, numeric-width selection,
  equal-width tie handling, and endpoint labels.
- Add behavior and static mutation-sensitive coverage.

## Implementation Units

### Probability Boundary

File: `rt_covid19.py`

- Validate the public probability argument before PMF shape or value work.
- Keep the validated value compatible with the existing cumulative-mass
  calculation and output labels.

### Regression Contract

Files: `tests/test_rt_covid19.py`, `scripts/check_notebook_provenance.py`

- Cover accepted Python and NumPy real scalar probabilities.
- Cover invalid types, non-finite values, booleans, and endpoints.
- Require the implementation, tests, documentation, and completed evidence.

### Documentation

Files: `README.md`, `CHANGES.md`

- Document the finite open-interval probability boundary without changing the
  historical educational-use warning.

## Verification

- focused probability tests and complete offline suite
- isolated repository and external-directory `make check`
- hostile probability-type, finite-value, endpoint, test, documentation, and
  completed-plan mutations
- exact diff, generated-artifact, bytecode, conflict-marker, and changed-line
  credential audits

## Scope Boundaries

- Do not change dataset loading, case preparation, posterior generation, PMF
  normalization, interval search, notebook outputs, or dependency pins.
- Do not merge or close stacked pull requests without explicit authorization.

## Verification Results

- The focused HDI probability tests passed, and the complete offline suite
  passed 23 tests.
- The isolated `make check` passed from the repository and an external
  directory with global `PYTHONPATH` removed, covering provenance validation,
  Ruff formatting and lint, notebook JSON, dependency integrity, and zero known
  vulnerabilities from `pip-audit`.
- Seven hostile probability mutations were rejected across real-type, boolean,
  finite-value, endpoint, stable-message, README-index, and completed-plan
  contracts.
- Final exact-diff, generated-artifact, bytecode, conflict-marker, and
  changed-line credential audits found only intended paths and no artifacts.
