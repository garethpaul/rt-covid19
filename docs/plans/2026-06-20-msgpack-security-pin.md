# msgpack Verification Security Pin

Status: Completed

## Context

The exact Python 3.12 verification environment resolved `msgpack 1.1.2`
through `pip-audit` and CacheControl. A fresh `pip-audit` run reported
GHSA-6v7p-g79w-8964 and identified 1.2.1 as the fixed release.

## Work Completed

- Added an exact `msgpack 1.2.1` development requirement.
- Extended the notebook provenance checker so removing or changing the pin
  fails the canonical gate.
- Documented the transitive verification-tool boundary in the README,
  security guidance, and change history.

## Verification

- Installed `requirements.txt` and `requirements-dev.txt` in a fresh Python
  3.12 virtual environment with the host `PYTHONPATH` removed.
- `make check` passed from the repository root and an external directory.
- `pip check` reported no broken requirements.
- `pip-audit` reported no known vulnerabilities.
- The offline model suite, Ruff checks, notebook provenance check, and notebook
  JSON validation passed.
