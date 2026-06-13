# HDI Numeric Width Selection

## Status: Planned

## Context

`highest_density_interval` accepts any finite, strictly increasing numeric grid,
including nonuniform grids. Candidate intervals are currently compared by index
span, so equal-bin candidates can select a much wider numeric interval even
when a narrower interval contains the requested probability mass.

## Priority

The helper promises the narrowest interval, and custom nonuniform grids are an
explicitly supported validated input. Selection must therefore compare endpoint
distance on the actual grid rather than treating every adjacent point as the
same width.

## Objectives

- Compare candidate intervals by numeric endpoint width.
- Preserve the first interval when numeric widths tie.
- Keep PMF normalization, probability validation, and endpoint labels stable.
- Add focused uniform and nonuniform grid coverage.
- Protect the numerical decision with mutation-sensitive source and test
  contracts.

## Implementation Units

### U1. Characterize nonuniform interval selection

**Goal:** Demonstrate a PMF where equal-bin candidates have different numeric
widths and require the later, narrower interval.

**Files:** `tests/test_rt_covid19.py`

**Approach:** Use a small deterministic nonuniform grid whose first qualifying
candidate spans a large grid gap while a later candidate contains the same
requested mass over a smaller endpoint distance.

**Test scenarios:**

- Nonuniform candidates select the smallest numeric width.
- Existing uniform-grid behavior and integer endpoint identity remain stable.
- Equal numeric widths preserve the earliest qualifying interval.

**Verification:** The nonuniform regression fails under the current index-span
comparison and passes only when endpoint widths drive selection.

### U2. Select HDIs by endpoint distance

**Goal:** Make the implementation match its narrowest-interval contract.

**Dependencies:** U1

**Files:** `rt_covid19.py`, `tests/test_rt_covid19.py`

**Approach:** Compute each candidate's width from the already validated numeric
grid and replace the current best only when that width is strictly smaller.

**Patterns to follow:** Reuse the existing validated `grid` array and preserve
the current left-to-right candidate scan for deterministic ties.

**Verification:** Focused tests pass and hostile mutations restoring index-span
comparison or reversing the strict tie rule are rejected.

### U3. Synchronize numerical-contract evidence

**Goal:** Keep maintenance documentation and provenance checks aligned with the
implemented selection rule.

**Dependencies:** U1, U2

**Files:** `README.md`, `VISION.md`, `CHANGES.md`,
`scripts/check_notebook_provenance.py`,
`docs/plans/2026-06-13-hdi-numeric-width.md`

**Approach:** Document numeric-width HDI selection and record actual validation
only after implementation succeeds.

**Verification:** The canonical plan/provenance checker and `make check` pass.

## Scope Boundary

This change does not redefine highest-density probability mass, require uniform
grids, alter the notebook's default Rt range, or change DataFrame recursion.
