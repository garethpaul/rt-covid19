# Data Source URL Constant

## Status: Completed

## Context

The notebook reads NYT county case data from a checked-in HTTPS URL. That URL
was assigned to a generic local variable, while the README and provenance notes
treat it as a source contract. A named constant makes the runtime download
source easier to audit without executing the notebook.

## Objectives

- Keep the notebook runtime behavior unchanged.
- Name the NYT county CSV source as `DATA_SOURCE_URL`.
- Require `pandas.read_csv` to use that named source constant.
- Preserve source-only notebook checks without refreshing data.

## Work Completed

- Replaced the notebook's generic `url` variable with `DATA_SOURCE_URL`.
- Extended `scripts/check_notebook_provenance.py` to require the constant and
  `pd.read_csv(DATA_SOURCE_URL, ...)` usage.
- Updated README, DATA_PROVENANCE, VISION, and CHANGES notes for the source URL
  constant guard.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make lint`
- `make check`
- `make verify`
- `git diff --check`
