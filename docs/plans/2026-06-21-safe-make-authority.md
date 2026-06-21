# Safe Make Authority

## Status: Completed

## Context

The Make root split checkout paths containing spaces, while caller-controlled
root, Python, shell, preload, and Makefile-list authority could redirect verification.

## Scope Boundaries

- Do not change model behavior, notebook content, data provenance, dependencies, or CI runtime.
- Preserve Python 3.12, frozen binary-only installation, and full dependency audit.

## Work Completed

- Canonicalize the checked-in Makefile without splitting shell-sensitive paths.
- Freeze Python and shell authority, export the root as data, and reject preloaded or ambiguous Makefiles.
- Add the dependency-free authority suite to `make verify` and `make check`.

## Verification Completed

- Python 3.12 passed root and external `make check` runs.
- All 63 executed target, root, shell, and Python authority cases passed.
- Both `MAKEFILE_LIST` override channels, a `MAKEFILES` preload, and an
  ambiguous multiple-Makefile invocation failed closed.
- Model, notebook, provenance, tests, lint, dependency audit, `git diff --check`, and Git object validation passed.
