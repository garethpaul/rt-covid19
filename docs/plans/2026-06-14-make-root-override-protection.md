# Make Root Override Protection

## Status: Planned

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
