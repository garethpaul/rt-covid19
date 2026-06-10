# Data Provenance

## Source

The notebook reads county-level COVID-19 case data from:

`https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv`

The file is downloaded at notebook runtime through `rt_covid19.load_counties`,
which uses `pandas.read_csv`. The helper names this runtime source as
`DATA_SOURCE_URL`. The repository does
not commit a local copy of the dataset. Notebook, provenance, and local runtime
configuration URL references should use HTTPS.
The maintained loader accepts only the configured HTTPS GitHub source for live
downloads, uses a 30-second timeout, and caps the response at 512 MiB by
default. Redirects are rejected so credentials or data requests cannot cross
the documented source boundary. Tests pass in-memory file objects instead of
making network requests.

## Refresh Status

No data refresh was performed on 2026-06-08. Because the notebook reads the NYT
`master` branch at runtime, results depend on the date and network response of
the notebook execution environment.

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

- reads county, date, and case-count columns;
- indexes the data by county and date;
- starts each county after the last zero-case day;
- applies Gaussian smoothing to reduce reporting noise before estimating Rt.

## Presentation Defaults

The notebook defines neutral plotting defaults for filtered regions, lockdown
status groups, and summary colors so later visualization cells have explicit
inputs. The defaults do not encode current policy or public-health status.

## Interpretation

This repository is a historical educational analysis, not current public-health guidance.
Results should be interpreted with the notebook's model assumptions, uncertainty
intervals, stale-source risk, and reporting-noise limitations in mind.
