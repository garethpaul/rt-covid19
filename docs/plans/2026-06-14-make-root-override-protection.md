# Make Root Override Protection

## Status: Completed

## Context

The Makefile derives its repository root from the loaded file and uses it for
notebook, model, dependency, and audit gates. GNU Make command-line variables
outrank an ordinary assignment, so `make ROOT=/tmp check` can redirect those
commands away from the checkout and weaken location-independent verification.

## Requirements

- **R1:** Prevent command-line and environment values from replacing the
  Makefile-derived repository root.
- **R2:** Keep the `PYTHON` interpreter configurable.
- **R3:** Require the exact protected declaration in the provenance checker.
- **R4:** Prove the full gate from the checkout and an external directory with
  a hostile `ROOT` argument.
- **R5:** Preserve notebook provenance, dataset integrity, numerical behavior,
  dependency auditing, and hosted workflow policy.

## Implementation Units

### U1. Protected Root

Give the repository-derived root override precedence without changing recipes
or tool selection.

### U2. Provenance Contract

Extend `scripts/check_notebook_provenance.py` to reject weakened, duplicate,
displaced, or caller-controlled root declarations and incomplete evidence.

### U3. Verification

Run focused provenance checks, all Make aliases from root and externally,
Python 3.12 validation, hostile mutations, and integrity screening.

## Scope Boundary

- Do not modify the notebook, data snapshot, model, tests, or dependencies.
- Do not change workflow actions, permissions, runtime, or coverage.
- Do not add generated notebook output, caches, or credentials.

## Verification

- `python3 scripts/check_notebook_provenance.py`
- `make check`
- `make ROOT=/tmp check` from an external directory
- root-declaration, checker, plan-status, README-index, and evidence mutations
- Python syntax, workflow YAML, protected-file, secret, artifact, and
  `git diff --check` gates

## Work Completed

- Protected the Makefile-derived repository root from command-line and
  environment overrides while preserving configurable Python selection.
- Added exact declaration, completed-evidence, and README-index contracts.
- Preserved notebook, model, dataset, dependency, and hosted-workflow behavior.

## Verification Results

- `python3 scripts/check_notebook_provenance.py` passed.
- From both the checkout and an external directory, all six public Make aliases passed.
- `make ROOT=/tmp check` passed externally while still running repository-owned
  provenance, model, notebook, and dependency gates.
- A disposable exact-pinned Python 3.12 environment with `PYTHONPATH` unset
  completed Ruff, 19 tests, notebook JSON validation, `pip check`, and
  `pip-audit` with no known vulnerabilities.
- Six hostile mutations were rejected across root declaration, checker
  expectation, plan status, README indexing, and recorded evidence.
- Python syntax, workflow YAML, exact-base protected-file comparison, secret
  screening, generated-artifact screening, and `git diff --check` passed before
  shipping.
