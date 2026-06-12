# Changes

## 2026-06-10

- Extracted reusable data loading and Rt calculations into a tested module.
- Modernized the notebook to pandas 3 and pinned the Python 3.12 runtime.
- Corrected the highest-density interval's low-bound off-by-one behavior.
- Removed invalid escape warnings from notebook mathematical labels.
- Added bounded, timed, host-restricted, non-redirecting dataset downloads.
- Added ten offline unit tests, Ruff, dependency auditing, and CI.
- Added installed-dependency consistency checks, root-independent Make targets,
  a fixed hosted runner, and cancellation of superseded CI runs.
- Disabled persisted checkout credentials and made the reviewed verification
  workflow an exact single-file repository contract.
- Rejected negative or duplicate custom Rt grid values before posterior
  calculations, with focused numerical regression and source-contract coverage.

## 2026-06-09

- Converted Matplotlib runtime configuration comment links to HTTPS and added
  validation coverage for that file.
- Named the notebook's NYT CSV runtime source as `DATA_SOURCE_URL` and added
  provenance validation for the constant and `read_csv` usage.
- Added HTTPS-only URL validation for notebook, README, and data provenance
  references.
- Required `matplotlibrc` to use the Agg backend for headless historical
  notebook reproduction.
- Added validation and provenance notes for the `pandas<2` constraint required
  by the notebook's legacy `read_csv(..., squeeze=True)` usage.
- Added notebook kernel-version provenance checks so README and
  `DATA_PROVENANCE.md` document the recorded Python 3.6.7 runtime context.
- Removed empty trailing notebook code cells and added validation so committed
  source-only notebooks do not carry unfinished analysis placeholders.

## 2026-06-08

- Added neutral notebook presentation defaults and validation so summary
  plotting cells do not depend on undefined symbols.
- Stripped stale notebook outputs and execution counts, and made the provenance
  checker enforce source-only notebook commits.
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
