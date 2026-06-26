# Preserve Trailing Zero-Case Days

Status: Completed 2026-06-26.

## Problem

`prepare_cases` started model input after the last smoothed zero day. A valid
cumulative series ending in a short reporting plateau therefore produced an
empty result, discarding earlier positive observations solely because the most
recent days reported no new cases.

The posterior calculation cannot accept a zero observation followed by a
positive observation because that transition has zero Poisson likelihood under
the existing model. A terminal run of zeros does not create that transition and
should remain available to the analysis.

## Approach

- Find the final positive smoothed observation.
- Trim through the last zero before that positive observation.
- Preserve zero observations after the final positive observation.
- Preserve the existing empty result for an all-zero smoothed series.
- Protect the behavior with a focused regression and static source contracts.

## Alternatives Considered

- Starting at the first positive observation leaves later zero-to-positive
  transitions in the likelihood input.
- Rejecting every series with an interior zero would discard a usable suffix
  rather than retaining observations after the final invalid transition.
- Replacing zeros with an arbitrary floor changes the statistical inputs and
  model semantics.

## Files

- `rt_covid19.py`
- `tests/test_rt_covid19.py`
- `scripts/check_notebook_provenance.py`
- `DATA_PROVENANCE.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-26-trailing-zero-case-preprocessing.md`

## Verification

- Confirm the focused regression fails before implementation because an
  eight-day cumulative series ending in a three-day plateau returns no rows.
- Run the focused regression and complete synthetic unit-test suite.
- Run Ruff formatting and linting, notebook provenance validation, notebook
  JSON validation, dependency consistency, dependency audit, and Make root
  authority checks through `make check` on Python 3.12.
- Run the absolute-Makefile gate from outside the repository.
- Mutate the implementation back to the last-zero cutoff and confirm the
  regression or provenance contract rejects it.

## Scope Boundaries

- Do not change smoothing parameters, posterior likelihoods, priors, Rt grids,
  HDI behavior, dataset identity, notebook outputs, dependencies, or workflow
  structure.
- Do not fetch current health data or present historical estimates as current
  public-health guidance.

## Success Criteria

- A cumulative series ending in zero new cases retains its positive history and
  terminal zero observations.
- A zero followed by a later positive observation remains outside the returned
  model input.
- An all-zero smoothed series retains the existing empty result.

## Work Completed

- Replaced the global last-zero cutoff with a final-positive-aware boundary.
- Added the focused plateau regression and mutation-sensitive source contracts.
- Updated preprocessing provenance, roadmap guidance, and the changelog.

## Verification Completed

- The pre-fix focused regression failed because the returned smoothed series
  was empty.
- Both focused boundary regressions and the complete 37-test synthetic model
  suite passed.
- Ruff format and lint, notebook provenance and JSON validation, `pip check`,
  and `pip-audit` passed through `make check` on Python 3.12.
- The same `make check` gate passed through the absolute Makefile path from an
  external directory.
- Restoring the old global last-zero cutoff failed the trailing-zero regression.
