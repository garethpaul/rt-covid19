# Gate Execution and Gating Observation

## Status: Completed

## Context

The repository gate asserted that runner source text exists, but nothing asserted that
`make check` actually executes those runners and fails when they fail. The Makefile pins
were substring pins, and `verify`'s prerequisite list and the `unittest` recipe line were
not pinned at all. Four independent single-line edits therefore removed verification while
`make check` exited 0 and printed every success banner:

| Mutation | Before | After |
| --- | --- | --- |
| `verify: root-test lint test build` -> `verify: root-test lint build` | exit 0, 0 of 37 tests ran | exit 1, `make check never invoked a quality runner matching '-m unittest'` |
| `... -m unittest ... \|\| true` | exit 0, suite reported `FAILED (failures=1)` | exit 1, `make check ignored a failing '-m unittest' runner and still exited 0` |
| `-$(RUN_IN_REPO) $(PYTHON) -m unittest ...` (make error-ignore prefix) | exit 0, suite reported failure | exit 1, same propagation assertion |
| `... check_notebook_provenance.py \|\| true` | exit 0, checker printed `provenance checks failed` | exit 1, `make check ignored a failing 'scripts/check_notebook_provenance.py' runner` |

A planted defect confirmed the gap was load-bearing rather than theoretical: widening
`load_counties`'s negative-total rejection from `(counties < 0)` to `(counties < -1000000)`
made `load_counties` return a `-1` case total. The unmodified gate caught it
(`FAILED (failures=1)`); with `test` severed from `verify` the same defect passed at exit 0.

`scripts/test-makefile-root.sh` was also stubbable: only its Makefile invocation line was
pinned, never its body, so a three-line script printing the success banner satisfied the gate.

## Scope Boundaries

- Do not change model behavior, notebook content, data provenance, dependencies, or CI runtime.
- Preserve Python 3.12, frozen binary-only installation, and full dependency audit.

## Work Completed

- Add failure-injection propagation to the authority observer. The fake `python3` now fails
  on demand for a matched argument pattern, and each public alias must both dispatch the
  matching runner and fail because it failed. This observes execution and gating at the
  which-arguments level, which no source pin can reach.
- Require the `verify` and `check` prerequisite lines and every recipe invocation line to
  match as exact whole lines, closing `|| true`, the `-cmd` prefix, and severed prerequisites
  in the source.
- Pin `scripts/test-makefile-root.sh` by SHA-256 so a banner-printing stub is rejected.
- Add two out-of-band CI steps that invoke the observer and the contract checker directly.
  `make check` cannot police its own wiring: severing both `root-test` and `lint` from
  `verify` runs neither detector. Total disconnection is detectable only from outside the
  disconnected path.

The two layers are complementary and mutually cross-guarding. The executed observer proves
source equals effective recipe and catches a neutered verdict on the checker's own invoking
line; the checker's whole-line pins and digest catch the observer being disconnected or
stubbed. Neither is downstream of the other's blast radius alone.

## Verification Completed

- Python 3.12 passed `make verify`; 37 model tests, lint, provenance, and build all green.
- All 63 executed target, root, shell, and Python authority cases still pass, plus 12 new
  injected runner-failure cases, each failing its alias.
- Six hostile gate mutations were rejected with the correct specific diagnostic: severed
  `test`, severed `root-test`, severed `root-test` and `lint` together, `|| true` on the
  `unittest` line, the `-cmd` error-ignore prefix, `|| true` on the checker's own line, and
  a stubbed observer.
- `make dependencies` was not run locally: `python3 -m pip check` reports a pre-existing
  conflict in the audit environment (`awscli`/`botocore`), and `pip_audit` needs network
  access. Both run unchanged in CI.
</content>
