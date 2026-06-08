# Rt Covid19 Baseline

## Status: Completed

## Context

`rt-covid19` is a historical educational notebook for estimating effective
COVID-19 reproduction numbers from county case data. Because the notebook reads
external data at runtime, repository health depends on visible provenance,
explicit dependency notes, and clear non-guidance language.

## Objectives

- Preserve the notebook narrative and statistical assumptions.
- Keep the NYT county data URL visible in the notebook, README, and provenance
  notes.
- Validate notebook JSON and dependency documentation without executing a data
  refresh.
- Make the historical, non-current-public-health-guidance status explicit.
- Maintain completed maintenance plans under `docs/plans`.

## Work Completed

- Confirmed `make check` validates notebook JSON, requirements, and provenance.
- Added canonical `docs/plans` coverage for the current notebook baseline.
- Extended the provenance checker to require completed `docs/plans` entries
  with `make check` verification.
- Updated README, VISION, and CHANGES to make the baseline discoverable.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `python3 -m json.tool Rt-covid19.ipynb`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Move reusable Rt calculations into importable functions with unit tests.
- Add environment constraints beyond `requirements.txt` if the notebook is
  refreshed.
