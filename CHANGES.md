# Changes

## 2026-06-08

- Added `make check` as the shared repository verification alias.
- Added a notebook provenance check for dependency coverage, notebook JSON, and
  the visible NYT county data source.
- Added `requirements.txt` for the notebook imports, with `pandas<2` for the
  legacy `read_csv(..., squeeze=True)` usage.
- Documented the data source and clarified that the notebook is not current
  public-health guidance.
- Added `make verify` as the repository verification command.
- Added `DATA_PROVENANCE.md` with runtime download, refresh status,
  preprocessing, and interpretation notes.
- Added canonical `docs/plans` coverage and made the notebook provenance
  checker require completed plans.
