# Data Provenance

## Source

The notebook reads county-level COVID-19 case data from:

`https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv`

The file is downloaded at notebook runtime with `pandas.read_csv`. The
repository does not commit a local copy of the dataset.

## Refresh Status

No data refresh was performed on 2026-06-08. Because the notebook reads the NYT
`master` branch at runtime, results depend on the date and network response of
the notebook execution environment.

## Preprocessing

The notebook:

- reads county, date, and case-count columns;
- indexes the data by county and date;
- starts each county after the last zero-case day;
- applies Gaussian smoothing to reduce reporting noise before estimating Rt.

## Interpretation

This repository is a historical educational analysis, not current public-health guidance.
Results should be interpreted with the notebook's model assumptions, uncertainty
intervals, stale-source risk, and reporting-noise limitations in mind.
