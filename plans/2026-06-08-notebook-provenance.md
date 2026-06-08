# Notebook Provenance

## Problem

The repository contained a COVID-19 Rt notebook without an environment file or
README provenance for the remote county case data it reads. The README also did
not clearly say that the historical notebook is not current public-health
guidance.

## TDD Evidence

1. Added `scripts/check_notebook_provenance.py` and wired it to `make lint`.
2. Ran the checker before documentation fixes and confirmed it failed on the
   missing `requirements.txt`, missing README data-source URL, and missing
   public-health guidance caveat.
3. Added the dependency manifest and README provenance notes, then reran the
   verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `git diff --check`
