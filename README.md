# rt-covid19

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/rt-covid19` is a data science notebook project. This repo contains a notebook to track the progression of COVID19 is the effective repro number (Rt).

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: no dominant source language detected.

## Repository Contents

- `README.md` - project overview and local usage notes
- `CHANGES.md` - maintenance history for notebook provenance checks
- `DATA_PROVENANCE.md` - data source, refresh, and interpretation notes
- `Makefile` - local verification entry points
- `Rt-covid19.ipynb` - historical educational notebook
- `docs/plans` - completed maintenance plans for the current baseline
- `plans` - historical implementation notes
- `requirements.txt` - notebook runtime dependencies
- `requirements-dev.txt` - pinned verification dependencies
- `rt_covid19.py` - reusable, tested data-loading and Rt model helpers
- `tests` - offline synthetic-data model tests
- `scripts` - provenance and notebook validators
- `SECURITY.md` - security reporting and disclosure guidance
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: no top-level source directories detected
- Dependency and build manifests: requirements.txt
- Entry points or build surfaces: none detected
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git
- Python 3.12 for the maintained runtime and verification gate
- The checked-in notebook metadata records a Python 3.6.7 kernel; use a
  compatible environment only when reproducing its original historical setup.

### Setup

```bash
git clone https://github.com/garethpaul/rt-covid19.git
cd rt-covid19
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
```

The development requirements pin `msgpack 1.2.1` across `pip-audit`'s
CacheControl dependency so the verification environment does not resolve the
vulnerable 1.1.2 release.

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `Rt-covid19.ipynb` in Jupyter or another compatible notebook viewer.
- The notebook reads county case data from `https://raw.githubusercontent.com/nytimes/covid-19-data/62ef34cfcb60214be873a38d73619da9ea57d50b/us-counties.csv`.
  The source cell names that runtime CSV download as `DATA_SOURCE_URL`.
- See `DATA_PROVENANCE.md` for runtime download behavior, preprocessing notes,
  and refresh status.
- The notebook metadata records Python 3.6.7 as the historical kernel version.
- The maintained runtime uses pinned Python 3.12-compatible dependencies and
  the supported `DataFrame.squeeze("columns")` pandas API.
- Live data loading requires the configured HTTPS GitHub URL, applies a
  30-second request timeout, rejects redirects, and caps downloads at 512 MiB
  by default. Before parsing, it requires the reviewed 104,795,654-byte
  snapshot with SHA-256
  `dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0`.
- `matplotlibrc` sets the Agg backend for headless historical reproduction
  runs.
- The committed notebook is source-only: execution counts and rendered outputs
  are intentionally stripped to avoid presenting stale results as a refresh.
- This is a historical educational analysis and is not current public-health guidance.

## Testing and Verification

- `make check` validates notebook JSON, provenance, formatting, lint, seventeen
  offline model tests, bytecode compilation, and declared dependencies.
- `make check` also rejects stored notebook outputs and execution counts.
- `make check` also rejects empty code cells so the source-only notebook does
  not carry unfinished analysis placeholders.
- `make check` also verifies that summary-plot presentation defaults are
  defined in the notebook.
- `make check` also verifies that README and provenance notes document the
  notebook's recorded Python 3.6.7 kernel version.
- `make check` also rejects removed `read_csv(squeeze=True)` behavior and
  protects the tested helper-module boundary.
- `make check` also verifies that `matplotlibrc` keeps the headless Agg
  backend configured.
- `make check` also verifies that notebook, provenance, and Matplotlib runtime
  configuration URL references use HTTPS.
- `make check` also verifies that the NYT runtime CSV URL and data loading stay
  centralized in `rt_covid19.load_counties`.
- County ingestion requires real numeric, non-boolean county case totals before
  finite and non-negative value checks.
- County ingestion preserves state-qualified county identity with a unique,
  non-missing `(state, county, date)` index so same-name counties cannot merge.
- `make check` also requires NYT commit
  `62ef34cfcb60214be873a38d73619da9ea57d50b`, the 104,795,654-byte snapshot,
  and SHA-256 `dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0`
  before remote CSV parsing.
- `make check` also requires numeric, finite, strictly increasing HDI grids
  before interval endpoints are returned.
- HDI probability masses must use real numeric, non-boolean values before
  interval selection.
- HDI probability mass must be a finite real number strictly between zero and
  one; booleans and non-numeric values are rejected at the model boundary.
- `make check` also requires HDI candidates on nonuniform grids to be compared
  by numeric endpoint width while preserving the earliest equal-width result.
- `make check` also requires one-dimensional, non-missing, unique, increasing
  case indexes before preprocessing or posterior calculations.
- Case preprocessing requires real numeric, non-boolean cumulative cases before
  differencing or smoothing. It also requires finite cumulative cases and
  non-negative cumulative cases.
- Posterior calculations require real numeric, non-boolean smoothed cases before
  floating-point conversion.
- GitHub Actions runs the same gate on Python 3.12 for pushes and pull requests.
- The canonical gate also runs `pip check`, and hosted installs require binary
  distributions on a fixed Ubuntu 24.04 runner.
- The single approved workflow uses immutable actions, read-only permissions,
  and checkout with persisted GitHub credentials disabled.
- `make check` also requires completed canonical plans under `docs/plans`.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- The scan did not identify production authentication, payment, or secret-management code. Treat future additions in those areas as security-sensitive.

## Maintenance Notes

- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-rt-covid19-baseline.md` for the canonical
  notebook provenance baseline.
- See `docs/plans/2026-06-08-strip-notebook-outputs.md` for the source-only
  notebook output policy.
- See `docs/plans/2026-06-08-notebook-presentation-defaults.md` for the
  summary-plot default guard.
- See `docs/plans/2026-06-09-empty-code-cell-guard.md` for the empty code-cell
  guard.
- See `docs/plans/2026-06-09-kernel-version-provenance.md` for the notebook
  kernel-version provenance guard.
- See `docs/plans/2026-06-09-pandas-squeeze-constraint.md` for the pandas
  compatibility guard.
- See `docs/plans/2026-06-10-modern-runtime-and-ci.md` for the tested model
  extraction, modern pandas runtime, and CI gate.
- See `docs/plans/2026-06-10-hosted-validation-hardening.md` for the fixed
  runner, root-independent gate, and dependency consistency checks.
- See `docs/plans/2026-06-09-matplotlib-headless-backend.md` for the
  Matplotlib headless backend guard.
- See `docs/plans/2026-06-09-https-url-provenance.md` for the HTTPS URL
  provenance guard.
- See `docs/plans/2026-06-09-data-source-url-constant.md` for the notebook data
  source URL constant guard.
- See `docs/plans/2026-06-09-matplotlibrc-https-urls.md` for the Matplotlib
  runtime configuration HTTPS URL guard.
- See `docs/plans/2026-06-10-rt-grid-validation.md` for the custom Rt grid
  numerical input guard.
- See `docs/plans/2026-06-12-hdi-grid-validation.md` for finite, strictly
  increasing HDI grids.
- See `docs/plans/2026-06-12-dataset-snapshot-integrity.md` for the immutable
  NYT commit, byte-size, and SHA-256 verification boundary.
- See `docs/plans/2026-06-13-case-index-ordering.md` for deterministic
  preprocessing and posterior observation indexes.
- See `docs/plans/2026-06-13-hdi-numeric-width.md` for nonuniform-grid HDI
  endpoint-width selection.
- See `docs/plans/2026-06-14-make-root-override-protection.md` for the
  caller-resistant, location-independent verification root.
- See `docs/plans/2026-06-14-hdi-frame-column-integrity.md` for non-empty,
  unambiguous posterior observation columns before HDI calculation.
- See `docs/plans/2026-06-14-hdi-probability-validation.md` for the finite real
  open-interval probability boundary.
- See `docs/plans/2026-06-15-smoothed-case-numeric-dtype.md` for real numeric,
  non-boolean smoothed cases at the posterior boundary.
- See `docs/plans/2026-06-16-cumulative-case-numeric-dtype.md` for real numeric,
  non-boolean cumulative cases at the preprocessing boundary.
- See `docs/plans/2026-06-16-cumulative-case-value-validation.md` for
  non-negative cumulative cases at the preprocessing boundary.
- See `docs/plans/2026-06-16-cumulative-case-finite-regression.md` for focused
  regression coverage of finite cumulative cases.
- See `docs/plans/2026-06-17-county-case-numeric-dtype.md` for real numeric,
  non-boolean county case totals at the ingestion boundary.
- See `docs/plans/2026-06-17-state-qualified-county-identity.md` for
  state-qualified county identity at ingestion and notebook selection.
- See `docs/plans/2026-06-20-msgpack-security-pin.md` for the patched
  verification-tool dependency boundary.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
