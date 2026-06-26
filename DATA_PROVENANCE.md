# Data Provenance

## Source

The notebook reads county-level COVID-19 case data from:

`https://raw.githubusercontent.com/nytimes/covid-19-data/62ef34cfcb60214be873a38d73619da9ea57d50b/us-counties.csv`

The file is downloaded at notebook runtime through `rt_covid19.load_counties`,
which uses `pandas.read_csv`. The helper names this runtime source as
`DATA_SOURCE_URL`. The repository does
not commit a local copy of the dataset. Notebook, provenance, and local runtime
configuration URL references should use HTTPS.
Ingested data must contain real numeric, non-boolean county case totals before
finite and non-negative value validation.
The maintained loader accepts only the configured HTTPS GitHub source for live
downloads, uses a 30-second timeout, and caps the response at 512 MiB by
default. Redirects are rejected so credentials or data requests cannot cross
the documented source boundary. The reviewed file is Git blob
`b20a210d4933a99f2bebb855b965f649ac871a40`, is 104,795,654 bytes, and has
SHA-256 `dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0`.
Remote bytes must match that size and digest before CSV parsing. Tests pass
in-memory file objects instead of making network requests; explicit local paths
and file-like objects remain caller-controlled and are not checked against the
remote snapshot identity.

## Refresh Status

No data refresh was performed on 2026-06-08. On 2026-06-12, the existing final
NYT repository state was recorded at commit
`62ef34cfcb60214be873a38d73619da9ea57d50b`; runtime downloads now use that
immutable snapshot instead of following the mutable `master` branch. A future
dataset refresh requires a reviewed commit, size, digest, and provenance update.

The committed notebook is source-only. Execution counts and rendered outputs are
stripped so checked-in artifacts do not imply that a fresh dataset download or
public-health update occurred.
Empty code cells are also removed so the notebook does not contain unfinished
analysis placeholders.

## Runtime Environment

The checked-in notebook metadata records Python 3.6.7 as the historical kernel
version. The maintained and CI-tested runtime is Python 3.12 with exact package
pins in `requirements.txt`. Data loading uses the supported
`DataFrame.squeeze("columns")` API rather than the removed pandas squeeze
argument.
The checked-in `matplotlibrc` sets `backend : Agg` so reproduction runs can
render plots in headless environments without requiring an interactive display.

## Preprocessing

The notebook:

- reads state, county, date, and case-count columns;
- preserves state-qualified county identity in a unique, non-missing
  `(state, county, date)` index;
- starts each county after the last zero-case day that is followed by a later
  positive day, preserving terminal zero-case runs;
- applies Gaussian smoothing to reduce reporting noise before estimating Rt.

Reusable preprocessing and posterior helpers require one-dimensional,
non-missing, unique, increasing case indexes before order-sensitive operations.
Preprocessing also requires real numeric, non-boolean cumulative cases before
differencing or Gaussian smoothing and requires finite cumulative cases and
non-negative cumulative cases.

## Presentation Defaults

The notebook defines neutral plotting defaults for filtered regions, lockdown
status groups, and summary colors so later visualization cells have explicit
inputs. The defaults do not encode current policy or public-health status.

## Interpretation

This repository is a historical educational analysis, not current public-health guidance.
Results should be interpreted with the notebook's model assumptions, uncertainty
intervals, stale-source risk, and reporting-noise limitations in mind. Tested
interval summaries require real numeric, non-boolean probability masses on
numeric, finite, strictly increasing HDI grids.
