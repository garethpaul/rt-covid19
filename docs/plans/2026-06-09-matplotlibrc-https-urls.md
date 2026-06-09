# Matplotlibrc HTTPS URLs

## Status: Completed

## Context

`matplotlibrc` is part of the notebook reproduction environment because it sets
the headless Agg backend. The existing HTTPS guard covered the notebook, README,
and data provenance notes, but not this runtime configuration file, which still
contained cleartext documentation links in comments.

## Objectives

- Keep runtime configuration URL references on HTTPS.
- Extend the static provenance checker to scan `matplotlibrc`.
- Preserve the existing headless backend and source-only notebook checks.
- Avoid executing or refreshing the historical notebook.

## Work Completed

- Converted `matplotlibrc` comment URLs from `http://` to `https://`.
- Extended `scripts/check_notebook_provenance.py` to reject insecure URLs in
  `matplotlibrc`.
- Updated README, DATA_PROVENANCE, VISION, and CHANGES notes.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make lint`
- `make build`
- `make check`
- `make verify`
- `git diff --check`
