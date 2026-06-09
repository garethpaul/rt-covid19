# Kernel Version Provenance

## Status: Completed

## Context

`Rt-covid19.ipynb` records notebook metadata for a Python 3.6.7 kernel, but the
README and data provenance notes did not have to expose that runtime context.
Because the notebook uses legacy pandas behavior, the historical kernel version
is part of the reproducibility story.

## Objectives

- Keep the notebook metadata as the source of truth for the recorded kernel.
- Require README and data provenance notes to document the Python version.
- Preserve source-only notebook validation for outputs, execution counts, and
  empty code cells.
- Avoid refreshing data or rerunning the notebook in this documentation pass.

## Work Completed

- Extended `scripts/check_notebook_provenance.py` to read
  `metadata.language_info.version` from the notebook.
- Required README and `DATA_PROVENANCE.md` to mention the documented Python
  version.
- Added `Python 3.6.7` runtime notes to README and data provenance.
- Updated VISION and CHANGES notes for kernel-version provenance.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `make check`
- `make verify`
- `git diff --check`
