# Hosted Validation Hardening

Status: Completed

## Context

The modern Python 3.12 runtime, offline model tests, notebook checks, Ruff, and
dependency audit were already in place. The validation entrypoint still assumed
the caller's current directory, used a floating Ubuntu runner label, and did not
run `pip check` despite listing that command in the modernization plan.

## Objectives

- Make the canonical gate independent of the caller's working directory.
- Verify the installed dependency graph as well as known vulnerabilities.
- Fix the hosted runner image and cancel superseded runs.
- Keep action revisions immutable and make their reviewed versions visible.
- Prefer binary distributions during the hosted install.

## Work Completed

- Anchored Makefile paths and working directories to the repository root.
- Added `pip check` to the canonical dependency gate before `pip-audit`.
- Fixed GitHub Actions to Ubuntu 24.04 and added concurrency cancellation.
- Annotated the pinned checkout v6.0.3 and setup-python v6.2.0 commits.
- Required binary distributions during the exact-pinned hosted install.
- Extended the provenance checker to fail closed when these controls drift.

## Verification

- `make check`
- `make -f /path/to/repository/Makefile check` from outside the repository
- `git diff --check`
