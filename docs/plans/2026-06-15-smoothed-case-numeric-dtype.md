# Smoothed Case Numeric Dtype Validation

## Status: Planned

## Context

`get_posteriors` converts a smoothed-case Series directly to `float`. That
silently accepts object-backed numeric strings and boolean values as case
counts, even though `prepare_cases` requires numeric input and booleans are not
valid counts. The public posterior helper can therefore calculate plausible
results from invalid data instead of rejecting it at the model boundary.

## Requirements

- Require smoothed cases to use a numeric, non-boolean pandas dtype before
  converting values to floating point.
- Reject numeric strings, booleans, categorical values, datetimes, and other
  non-numeric dtypes with one stable `ValueError` message.
- Preserve finite, non-negative value validation and valid integer, floating,
  and NumPy numeric Series behavior.
- Preserve case-index, sigma, Rt-grid, posterior-normalization, and likelihood
  behavior.
- Add behavior and static mutation-sensitive coverage.

## Implementation Units

### Model Boundary

File: `rt_covid19.py`

- Validate the Series dtype before `to_numpy(dtype=float)` coercion.
- Keep value finiteness and non-negativity checks unchanged after dtype
  validation.

### Regression Contract

Files: `tests/test_rt_covid19.py`, `scripts/check_notebook_provenance.py`

- Cover object-backed numeric strings and boolean smoothed cases.
- Confirm valid integer and floating Series remain accepted.
- Protect the implementation, focused assertions, documentation, and completed
  plan evidence.

### Documentation

Files: `README.md`, `VISION.md`, `CHANGES.md`

- Document the numeric, non-boolean smoothed-case boundary.

## Verification

- focused posterior dtype tests and complete offline suite
- isolated repository and external-directory `make check`
- hostile numeric-dtype, boolean-bypass, regression, documentation, and
  completed-plan mutations
- exact diff, generated-artifact, bytecode, conflict-marker, and changed-line
  credential audits

## Scope Boundaries

- Do not change dataset loading, case smoothing, sigma or Rt-grid validation,
  posterior formulas, HDI calculation, notebook outputs, or dependency pins.
- Do not merge or close stacked pull requests without explicit authorization.
