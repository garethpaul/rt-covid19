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

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `Rt-covid19.ipynb` in Jupyter or another compatible notebook viewer.
- The notebook reads county case data from `https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv`.
  The source cell names that runtime CSV download as `DATA_SOURCE_URL`.
- See `DATA_PROVENANCE.md` for runtime download behavior, preprocessing notes,
  and refresh status.
- The notebook metadata records Python 3.6.7 as the historical kernel version.
- The maintained runtime uses pinned Python 3.12-compatible dependencies and
  the supported `DataFrame.squeeze("columns")` pandas API.
- Live data loading requires the configured HTTPS GitHub URL, applies a
  30-second request timeout, rejects redirects, and caps downloads at 512 MiB
  by default.
- `matplotlibrc` sets the Agg backend for headless historical reproduction
  runs.
- The committed notebook is source-only: execution counts and rendered outputs
  are intentionally stripped to avoid presenting stale results as a refresh.
- This is a historical educational analysis and is not current public-health guidance.

## Testing and Verification

- `make check` validates notebook JSON, provenance, formatting, lint, eleven
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

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
