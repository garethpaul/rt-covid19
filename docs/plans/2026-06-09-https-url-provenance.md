# HTTPS URL Provenance

## Status: Completed

## Context

The notebook and provenance notes include external references for the NYT data
source and background statistical material. Because the repository is preserved
as a historical data-science artifact, those references should avoid cleartext
HTTP URLs in committed notebook or provenance content.

## Objectives

- Require notebook source and markdown cells to use HTTPS URLs.
- Require README and `DATA_PROVENANCE.md` URL references to use HTTPS.
- Preserve the existing data-source documentation and source-only notebook
  checks without executing or refreshing the notebook.

## Work Completed

- Extended `scripts/check_notebook_provenance.py` to reject `http://` URLs in
  notebook cells, README, and data provenance notes.
- Split notebook source aggregation so assignment/import checks still operate
  only on code cells.
- Updated README, DATA_PROVENANCE, VISION, and CHANGES notes for the HTTPS URL
  guard.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `make verify`
- `git diff --check`
