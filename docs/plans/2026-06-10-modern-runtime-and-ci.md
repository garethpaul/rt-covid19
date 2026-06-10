# Modern Runtime and CI

## Status: Completed

## Context

The historical notebook had no automated CI, used removed pandas
`read_csv(squeeze=True)` behavior, and kept its reusable model calculations only
inside notebook cells without offline behavioral tests.

## Work Completed

- Extracted data loading, case preparation, Rt posterior calculation, and
  highest-density intervals into `rt_covid19.py` while keeping the notebook's
  narrative and plotting flow.
- Replaced the removed pandas squeeze argument with the supported
  `DataFrame.squeeze("columns")` API.
- Added synthetic-data unit tests for loading, validation, smoothing,
  posterior normalization, and interval calculation.
- Corrected the original highest-density interval low-bound off-by-one error
  and covered the expected narrow interval with a regression test.
- Escaped mathematical labels so maintained Python runs emit no invalid escape
  warnings.
- Added a 30-second timeout, 512 MiB cap, and exact HTTPS source guard around
  the live NYT dataset download, including redirect rejection.
- Pinned the verified Python 3.12 runtime and quality tools.
- Added Ruff, dependency auditing, and a least-privilege GitHub Actions gate
  using immutable Node 24 action references.

## Verification

- `make check`
- `python3 -m json.tool Rt-covid19.ipynb`
- `python3 -m pip check`
- `git diff --check`
