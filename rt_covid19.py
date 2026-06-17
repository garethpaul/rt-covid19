"""Reusable data loading and Rt model helpers from the project notebook."""

import hashlib
import math
import tempfile
import urllib.request
from numbers import Real
from urllib.parse import urlparse

import numpy as np
import pandas as pd
from scipy import stats as sps


DATA_SOURCE_COMMIT = "62ef34cfcb60214be873a38d73619da9ea57d50b"
DATA_SOURCE_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/62ef34cfcb60214be873a38d73619da9ea57d50b/us-counties.csv"
DATA_SOURCE_BYTES = 104_795_654
DATA_SOURCE_SHA256 = "dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0"
R_T_MAX = 12
R_T_RANGE = np.linspace(0, R_T_MAX, R_T_MAX * 100 + 1)
GAMMA = 1 / 7
DEFAULT_DOWNLOAD_TIMEOUT = 30
DEFAULT_MAX_DOWNLOAD_BYTES = 512 * 1024 * 1024
DOWNLOAD_CHUNK_SIZE = 1024 * 1024


def _validate_case_index(series, label):
    index = series.index
    if (
        index.nlevels != 1
        or index.hasnans
        or not index.is_unique
        or not index.is_monotonic_increasing
    ):
        raise ValueError(
            f"{label} index must be one-dimensional, non-missing, unique, and increasing."
        )


def _read_counties(source):
    return pd.read_csv(
        source,
        usecols=["date", "county", "state", "cases"],
        index_col=["state", "county", "date"],
        parse_dates=["date"],
    ).squeeze("columns")


def _download_counties(url, timeout, max_download_bytes):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https" or parsed_url.hostname != "raw.githubusercontent.com":
        raise ValueError("Remote county data must use the configured HTTPS GitHub host.")
    if parsed_url.username or parsed_url.password or parsed_url.query or parsed_url.fragment:
        raise ValueError("Remote county data URL must not contain credentials, query, or fragment.")
    if url != DATA_SOURCE_URL:
        raise ValueError("Remote county data URL must match DATA_SOURCE_URL.")

    request = urllib.request.Request(url, headers={"User-Agent": "rt-covid19/1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.geturl() != url:
            raise ValueError("County data download must not redirect to another URL.")
        content_length = response.headers.get("Content-Length")
        if content_length is not None:
            try:
                declared_size = int(content_length)
            except ValueError as exc:
                raise ValueError("County data Content-Length must be an integer.") from exc
            if declared_size < 0 or declared_size > max_download_bytes:
                raise ValueError("County data exceeds the configured download limit.")
            if declared_size != DATA_SOURCE_BYTES:
                raise ValueError("County data size does not match the reviewed snapshot.")

        downloaded_bytes = 0
        digest = hashlib.sha256()
        with tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024) as handle:
            while chunk := response.read(DOWNLOAD_CHUNK_SIZE):
                downloaded_bytes += len(chunk)
                if downloaded_bytes > max_download_bytes:
                    raise ValueError("County data exceeds the configured download limit.")
                digest.update(chunk)
                handle.write(chunk)
            if downloaded_bytes != DATA_SOURCE_BYTES:
                raise ValueError("County data size does not match the reviewed snapshot.")
            if digest.hexdigest() != DATA_SOURCE_SHA256:
                raise ValueError("County data SHA-256 does not match the reviewed snapshot.")
            handle.seek(0)
            return _read_counties(handle)


def load_counties(
    source=DATA_SOURCE_URL,
    timeout=DEFAULT_DOWNLOAD_TIMEOUT,
    max_download_bytes=DEFAULT_MAX_DOWNLOAD_BYTES,
):
    """Load county case totals as a state/county/date-indexed Series."""
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
        raise ValueError("Download timeout must be a positive finite number.")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Download timeout must be a positive finite number.")
    if not isinstance(max_download_bytes, int) or isinstance(max_download_bytes, bool):
        raise ValueError("Maximum download size must be a positive integer.")
    if max_download_bytes <= 0:
        raise ValueError("Maximum download size must be a positive integer.")

    if isinstance(source, str):
        scheme = urlparse(source).scheme
        if scheme in {"http", "https"}:
            counties = _download_counties(source, timeout, max_download_bytes)
        elif scheme:
            raise ValueError("County data source must be a local path or HTTPS URL.")
        else:
            counties = _read_counties(source)
    else:
        counties = _read_counties(source)

    if not isinstance(counties, pd.Series):
        raise ValueError("County data must contain exactly one cases column.")
    if counties.empty:
        raise ValueError("County data must contain at least one case row.")
    index = counties.index
    if (
        not isinstance(index, pd.MultiIndex)
        or list(index.names) != ["state", "county", "date"]
        or index.to_frame(index=False).isna().any().any()
        or not index.is_unique
    ):
        raise ValueError(
            "County data index must be unique, non-missing, and named state, county, date."
        )
    if (
        not pd.api.types.is_numeric_dtype(counties.dtype)
        or pd.api.types.is_bool_dtype(counties.dtype)
        or pd.api.types.is_complex_dtype(counties.dtype)
    ):
        raise ValueError("County case totals must use a real numeric, non-boolean dtype.")
    if not np.isfinite(counties.to_numpy(dtype=float)).all():
        raise ValueError("County case totals must be finite.")
    if (counties < 0).any():
        raise ValueError("County case totals must not be negative.")

    return counties.sort_index()


def prepare_cases(cases):
    """Convert cumulative case totals to raw and smoothed daily cases."""
    if not isinstance(cases, pd.Series) or cases.empty:
        raise ValueError("Cases must be a non-empty pandas Series.")
    _validate_case_index(cases, "Cases")
    if (
        not pd.api.types.is_numeric_dtype(cases.dtype)
        or pd.api.types.is_bool_dtype(cases.dtype)
        or pd.api.types.is_complex_dtype(cases.dtype)
    ):
        raise ValueError("Cases must use a real numeric, non-boolean dtype.")
    case_values = cases.to_numpy(dtype=float)
    if not np.isfinite(case_values).all():
        raise ValueError("Cases must contain finite values.")
    if (case_values < 0).any():
        raise ValueError("Cases must contain non-negative cumulative values.")

    new_cases = cases.diff()
    smoothed = (
        new_cases.rolling(7, win_type="gaussian", min_periods=1, center=True).mean(std=2).round()
    )

    zeros = smoothed.index[smoothed.eq(0)]
    idx_start = 0 if len(zeros) == 0 else smoothed.index.get_loc(zeros.max()) + 1
    smoothed = smoothed.iloc[idx_start:]
    return new_cases.loc[smoothed.index], smoothed


def get_posteriors(series, sigma=0.15, r_t_range=R_T_RANGE):
    """Calculate daily Rt posteriors and their cumulative log likelihood."""
    if not isinstance(series, pd.Series) or len(series) < 2:
        raise ValueError("Smoothed cases must be a pandas Series with at least two values.")
    _validate_case_index(series, "Smoothed cases")
    if (
        not pd.api.types.is_numeric_dtype(series.dtype)
        or pd.api.types.is_bool_dtype(series.dtype)
        or pd.api.types.is_complex_dtype(series.dtype)
    ):
        raise ValueError("Smoothed cases must use a real numeric, non-boolean dtype.")
    values = series.to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("Smoothed cases must contain finite, non-negative values.")
    if not isinstance(sigma, (int, float)) or isinstance(sigma, bool):
        raise ValueError("Sigma must be a positive finite number.")
    if not math.isfinite(sigma) or sigma <= 0:
        raise ValueError("Sigma must be a positive finite number.")

    r_t_range = np.asarray(r_t_range, dtype=float)
    if r_t_range.ndim != 1 or r_t_range.size == 0 or not np.isfinite(r_t_range).all():
        raise ValueError("Rt range must be a non-empty, finite one-dimensional array.")
    if (r_t_range < 0).any() or (np.diff(r_t_range) <= 0).any():
        raise ValueError("Rt range must be non-negative and strictly increasing.")

    lam = values[:-1] * np.exp(GAMMA * (r_t_range[:, None] - 1))
    likelihoods = pd.DataFrame(
        data=sps.poisson.pmf(values[1:], lam),
        index=r_t_range,
        columns=series.index[1:],
    )
    process_matrix = sps.norm(loc=r_t_range, scale=sigma).pdf(r_t_range[:, None])
    process_matrix /= process_matrix.sum(axis=0)

    prior = sps.gamma(a=4).pdf(r_t_range)
    prior /= prior.sum()
    posteriors = pd.DataFrame(index=r_t_range, columns=series.index, data={series.index[0]: prior})
    log_likelihood = 0.0

    for previous_day, current_day in zip(series.index[:-1], series.index[1:]):
        current_prior = process_matrix @ posteriors[previous_day]
        numerator = likelihoods[current_day] * current_prior
        denominator = float(numerator.sum())
        if not math.isfinite(denominator) or denominator <= 0:
            raise ValueError(f"Cannot normalize Rt posterior for {current_day!s}.")
        posteriors[current_day] = numerator / denominator
        log_likelihood += math.log(denominator)

    return posteriors, log_likelihood


def highest_density_interval(pmf, p=0.9):
    """Return the narrowest interval containing the requested probability."""
    if not isinstance(p, Real) or isinstance(p, (bool, np.bool_)):
        raise ValueError("Probability must be a finite real number strictly between zero and one.")
    p = float(p)
    if not math.isfinite(p) or not 0 < p < 1:
        raise ValueError("Probability must be a finite real number strictly between zero and one.")
    if isinstance(pmf, pd.DataFrame):
        if pmf.empty:
            raise ValueError("PMF DataFrame must contain rows and columns.")
        if pmf.columns.nlevels != 1 or pmf.columns.hasnans or not pmf.columns.is_unique:
            raise ValueError(
                "PMF DataFrame columns must be one-dimensional, non-missing, and unique."
            )
        return pd.DataFrame(
            [highest_density_interval(pmf[column], p=p) for column in pmf],
            index=pmf.columns,
        )
    if not isinstance(pmf, pd.Series) or pmf.empty:
        raise ValueError("PMF must be a non-empty pandas Series or DataFrame.")

    values = pmf.to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any() or values.sum() <= 0:
        raise ValueError("PMF values must be finite, non-negative, and have positive mass.")
    if (
        pmf.index.nlevels != 1
        or not pd.api.types.is_numeric_dtype(pmf.index.dtype)
        or pd.api.types.is_bool_dtype(pmf.index.dtype)
    ):
        raise ValueError("HDI grid must be numeric, finite, and strictly increasing.")
    grid = pmf.index.to_numpy(dtype=float)
    if not np.isfinite(grid).all() or (np.diff(grid) <= 0).any():
        raise ValueError("HDI grid must be numeric, finite, and strictly increasing.")
    values = values / values.sum()
    cumsum = np.concatenate(([0.0], np.cumsum(values)))
    best = None
    for low in range(len(values)):
        high = int(np.searchsorted(cumsum, cumsum[low] + p, side="left"))
        if high > len(values):
            break
        candidate = (low, high - 1)
        if best is None or (
            grid[candidate[1]] - grid[candidate[0]] < grid[best[1]] - grid[best[0]]
        ):
            best = candidate

    if best is None:
        raise ValueError("PMF does not contain the requested probability mass.")
    suffix = f"{p * 100:.0f}"
    return pd.Series(
        [pmf.index[best[0]], pmf.index[best[1]]],
        index=[f"Low_{suffix}", f"High_{suffix}"],
    )
