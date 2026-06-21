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
- Pass the Makefile path to recipes as environment data and resolve the root with
  POSIX shell built-ins instead of interpolating paths into shell source.
- Freeze Python and shell command overrides and reject preloaded or ambiguous
  Makefiles, including an additional `-f` before or after the repository file.
- Add the dependency-free authority suite to `make verify` and `make check`.

The selected Python executable still resolves through the provisioned `PATH` so
GitHub's setup-python runtime remains usable. The caller's toolchain `PATH` is a
trusted prerequisite; root resolution itself does not execute PATH-selected helpers.

## Verification Completed

- Python 3.12 passed root and external `make check` runs.
- All 63 executed target, root, shell, and Python authority cases passed.
- Both `MAKEFILE_LIST` override channels, a `MAKEFILES` preload, and ambiguous
  multiple-Makefile invocations in both `-f` orderings failed closed.
- Model, notebook, provenance, tests, lint, dependency audit, `git diff --check`, and Git object validation passed.
