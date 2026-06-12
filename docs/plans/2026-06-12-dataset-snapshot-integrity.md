# Dataset Snapshot Integrity

Status: Completed

## Context

Before this change, the historical notebook downloaded the NYT county dataset
from the mutable `master` branch. The loader constrained the host, URL,
redirects, timeout, and response size, but identical repository revisions could
still consume different bytes without detection if the upstream branch changed.

Primary-source inspection on 2026-06-12 found the NYT repository's `master`
head at commit `62ef34cfcb60214be873a38d73619da9ea57d50b`. The corresponding
`us-counties.csv` object is 104,795,654 bytes, Git blob
`b20a210d4933a99f2bebb855b965f649ac871a40`, and SHA-256
`dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0`.

## Priority

1. Pin the runtime dataset URL to an immutable upstream commit.
2. Verify the downloaded bytes before parsing them as county case data.
3. Preserve the existing host, credential, redirect, timeout, and size guards.
4. Make the source commit, object size, and checksum visible in provenance and
   repository contracts.
5. Keep live network execution outside the canonical offline test gate.

## Technical Approach

- Replace the branch-based data URL with the raw URL for the reviewed NYT
  commit while retaining `raw.githubusercontent.com` as the only remote host.
- Add an expected SHA-256 constant and compute the digest incrementally while
  the existing bounded download loop writes to its temporary file.
- Reject a digest mismatch before seeking or calling `pandas.read_csv`.
- Keep file-like objects and local paths checksum-free so tests and explicit
  local analysis remain offline and caller-controlled.
- Extend the provenance checker to require the immutable URL, checksum,
  completed plan, tests, and documentation as one reviewed contract.

## Implementation Units

### U1: Pin and verify the runtime dataset

Files: `rt_covid19.py`, `tests/test_rt_covid19.py`

- Introduce immutable source identity constants.
- Stream SHA-256 calculation through the bounded remote download path.
- Add positive and mismatch tests that prove parsing occurs only after a valid
  digest and that the existing transport controls remain intact.

### U2: Protect the repository contract

Files: `scripts/check_notebook_provenance.py`, `Rt-covid19.ipynb`

- Verify the unchanged notebook imports and calls continue using the maintained
  helper; no notebook source edit is required.
- Require the exact commit-pinned URL, SHA-256, test names, and implementation
  fragments so branch rollback or checksum bypass fails validation.

### U3: Record provenance and operational boundaries

Files: `README.md`, `DATA_PROVENANCE.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-12-dataset-snapshot-integrity.md`

- Record the upstream commit, Git blob identity, byte size, SHA-256, and the
  distinction between immutable remote reproduction and caller-supplied local
  inputs.
- Keep the historical-education and non-current-public-health warnings intact.

## Verification Strategy

- Run the focused loader tests for valid and mismatched checksums, redirect
  rejection, host restrictions, timeouts, and byte ceilings.
- Run `make check` with the pinned Python 3.12 dependency set.
- Run the gate from outside the checkout through the absolute Makefile path.
- Run a clean, network-isolated Python 3.12 environment after dependencies are
  available locally.
- Apply hostile mutations restoring the `master` URL, changing the checksum,
  bypassing digest validation, and weakening the mismatch test.
- Parse notebook JSON, workflow YAML, and overview SVG; run Python syntax,
  bytecode, secret, and `git diff --check` audits.

## Risks And Boundaries

- Pinning the final NYT repository snapshot intentionally stops implicit data
  refreshes. A future refresh requires a reviewed source commit, checksum, and
  provenance update.
- The live 100 MiB download is not part of every test run; exact primary-source
  metadata and one bounded checksum acquisition establish the reviewed input,
  while unit tests exercise digest behavior in memory.
- SHA-256 proves byte identity, not the correctness or completeness of the NYT
  dataset or the notebook's public-health interpretation.

## Work Completed

- Pinned `DATA_SOURCE_URL` to the reviewed NYT commit and recorded its Git blob,
  exact byte size, and SHA-256.
- Added early declared-size rejection plus final streamed byte-count and digest
  verification before CSV parsing.
- Preserved local path and file-like source behavior outside the remote
  snapshot contract.
- Added valid, size-mismatch, and digest-mismatch tests that prove parsing is
  blocked until remote identity verification succeeds.
- Extended the fail-closed repository checker and provenance documentation with
  the exact source identity and verification order.

## Verification Results

- A fresh Python 3.12 virtual environment installed every runtime and
  verification dependency from binary distributions at the exact declared
  versions.
- `make check` passed provenance contracts, Ruff formatting and lint, 15
  offline tests, notebook JSON, `pip check`, and `pip-audit` with no known
  vulnerabilities in that clean environment.
- The same complete gate passed through the absolute Makefile path from `/tmp`.
- A read-only, network-isolated `python:3.12.8` container passed `make verify`
  using a container-native environment populated from the exact pins.
- Four hostile mutations restoring the mutable `master` URL, changing the
  checksum, removing digest verification, or weakening the pre-parse assertion
  were rejected by the provenance checker.
- Primary-source retrieval of the pinned raw file returned 104,795,654 bytes
  with the recorded SHA-256.
- The plan-aware correctness, testing, maintainability, project-standards,
  security, reliability, and adversarial review found no actionable findings.
- Browser testing was not applicable because the repository has no served UI
  or browser route.
- Structured-file, syntax, staged/tracked-bytecode, secret, and
  `git diff --check` audits passed. Pre-existing ignored `__pycache__` files in
  the shared checkout were preserved and were not staged.

## Sources

- `https://github.com/nytimes/covid-19-data/commit/62ef34cfcb60214be873a38d73619da9ea57d50b`
- `https://github.com/nytimes/covid-19-data/blob/62ef34cfcb60214be873a38d73619da9ea57d50b/us-counties.csv`
