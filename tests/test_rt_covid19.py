import io
import hashlib
import math
import unittest
from unittest import mock

import numpy as np
import pandas as pd

import rt_covid19


class RtCovid19Tests(unittest.TestCase):
    def remote_response(self, payload, content_length=None):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = rt_covid19.DATA_SOURCE_URL
        response.headers = {} if content_length is None else {"Content-Length": content_length}
        response.read.side_effect = [payload, b""]
        return response

    def test_load_counties_returns_sorted_series(self):
        source = io.StringIO(
            "date,county,state,fips,cases,deaths\n"
            "2020-01-02,Alpha,CA,1,3,0\n"
            "2020-01-01,Alpha,CA,1,1,0\n"
        )

        counties = rt_covid19.load_counties(source)

        self.assertIsInstance(counties, pd.Series)
        self.assertEqual([1, 3], counties.tolist())
        self.assertEqual("cases", counties.name)

    def test_load_counties_rejects_negative_totals(self):
        source = io.StringIO("date,county,state,fips,cases,deaths\n2020-01-01,Alpha,CA,1,-1,0\n")

        with self.assertRaisesRegex(ValueError, "must not be negative"):
            rt_covid19.load_counties(source)

    def test_load_counties_rejects_non_real_numeric_dtypes(self):
        boolean_source = io.StringIO(
            "date,county,state,fips,cases,deaths\n"
            "2020-01-01,Alpha,CA,1,False,0\n"
            "2020-01-02,Alpha,CA,1,True,0\n"
        )
        with self.assertRaisesRegex(
            ValueError, "County case totals must use a real numeric, non-boolean dtype"
        ):
            rt_covid19.load_counties(boolean_source)

        string_source = io.StringIO(
            "date,county,state,fips,cases,deaths\n"
            "2020-01-01,Alpha,CA,1,one,0\n"
            "2020-01-02,Alpha,CA,1,two,0\n"
        )
        with self.assertRaisesRegex(
            ValueError, "County case totals must use a real numeric, non-boolean dtype"
        ):
            rt_covid19.load_counties(string_source)

        complex_counties = pd.Series([1 + 1j, 2 + 2j], dtype=np.complex128)
        with mock.patch("rt_covid19._read_counties", return_value=complex_counties):
            with self.assertRaisesRegex(
                ValueError, "County case totals must use a real numeric, non-boolean dtype"
            ):
                rt_covid19.load_counties(io.StringIO(""))

    def test_load_counties_accepts_real_numeric_dtypes(self):
        for dtype in (np.int64, np.float32):
            with self.subTest(dtype=dtype):
                expected = pd.Series([1, 3], index=[2, 1], name="cases", dtype=dtype)
                with mock.patch("rt_covid19._read_counties", return_value=expected):
                    counties = rt_covid19.load_counties(io.StringIO(""))

                self.assertEqual(dtype, counties.dtype.type)
                self.assertEqual([3, 1], counties.tolist())

    def test_load_counties_bounds_remote_download(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = rt_covid19.DATA_SOURCE_URL
        response.headers = {"Content-Length": "100"}

        with mock.patch("rt_covid19.urllib.request.urlopen", return_value=response) as urlopen:
            with self.assertRaisesRegex(ValueError, "download limit"):
                rt_covid19.load_counties(max_download_bytes=10, timeout=7)

        self.assertEqual(7, urlopen.call_args.kwargs["timeout"])

    def test_load_counties_rejects_unapproved_remote_url(self):
        with self.assertRaisesRegex(ValueError, "configured HTTPS GitHub host"):
            rt_covid19.load_counties("https://example.com/counties.csv")

    def test_load_counties_rejects_redirected_remote_url(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = "https://example.com/counties.csv"
        response.headers = {}

        with mock.patch("rt_covid19.urllib.request.urlopen", return_value=response):
            with self.assertRaisesRegex(ValueError, "must not redirect"):
                rt_covid19.load_counties()

    def test_load_counties_bounds_streamed_download(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = rt_covid19.DATA_SOURCE_URL
        response.headers = {}
        response.read.side_effect = [b"123456", b"789012", b""]

        with mock.patch("rt_covid19.urllib.request.urlopen", return_value=response):
            with self.assertRaisesRegex(ValueError, "download limit"):
                rt_covid19.load_counties(max_download_bytes=10)

    def test_load_counties_verifies_remote_snapshot_before_parsing(self):
        payload = b"date,county,state,fips,cases,deaths\n2020-01-01,Alpha,CA,1,1,0\n"
        response = self.remote_response(payload, str(len(payload)))

        with (
            mock.patch("rt_covid19.DATA_SOURCE_BYTES", len(payload)),
            mock.patch("rt_covid19.DATA_SOURCE_SHA256", hashlib.sha256(payload).hexdigest()),
            mock.patch("rt_covid19.urllib.request.urlopen", return_value=response),
        ):
            counties = rt_covid19.load_counties()

        self.assertEqual([1], counties.tolist())

    def test_load_counties_rejects_remote_snapshot_size_mismatch_before_parsing(self):
        payload = b"not-the-reviewed-snapshot"
        response = self.remote_response(payload, str(len(payload)))

        with (
            mock.patch("rt_covid19.DATA_SOURCE_BYTES", len(payload) + 1),
            mock.patch("rt_covid19._read_counties") as read_counties,
            mock.patch("rt_covid19.urllib.request.urlopen", return_value=response),
        ):
            with self.assertRaisesRegex(ValueError, "size does not match"):
                rt_covid19.load_counties()

        read_counties.assert_not_called()
        response.read.assert_not_called()

    def test_load_counties_rejects_remote_snapshot_digest_mismatch_before_parsing(self):
        payload = b"not-the-reviewed-snapshot"
        response = self.remote_response(payload)

        with (
            mock.patch("rt_covid19.DATA_SOURCE_BYTES", len(payload)),
            mock.patch("rt_covid19.DATA_SOURCE_SHA256", "0" * 64),
            mock.patch("rt_covid19._read_counties") as read_counties,
            mock.patch("rt_covid19.urllib.request.urlopen", return_value=response),
        ):
            with self.assertRaisesRegex(ValueError, "SHA-256 does not match"):
                rt_covid19.load_counties()

        read_counties.assert_not_called()

    def test_prepare_cases_returns_aligned_daily_series(self):
        index = pd.date_range("2020-01-01", periods=8)
        cases = pd.Series([1, 2, 4, 7, 11, 16, 22, 29], index=index)

        original, smoothed = rt_covid19.prepare_cases(cases)

        self.assertEqual(original.index.tolist(), smoothed.index.tolist())
        self.assertGreater(len(smoothed), 0)
        self.assertTrue(np.isfinite(smoothed).all())

    def test_prepare_cases_rejects_non_real_numeric_dtypes(self):
        index = pd.date_range("2020-01-01", periods=8)
        invalid_values = (
            pd.Series([False, True, True, True, True, True, True, True], index=index),
            pd.Series(np.arange(1, 9) + 1j, index=index),
        )

        for cases in invalid_values:
            with self.subTest(dtype=cases.dtype):
                with self.assertRaisesRegex(
                    ValueError,
                    "Cases must use a real numeric, non-boolean dtype",
                ):
                    rt_covid19.prepare_cases(cases)

    def test_prepare_cases_accepts_real_numeric_dtypes(self):
        index = pd.date_range("2020-01-01", periods=8)
        for dtype in (np.int64, np.float32):
            with self.subTest(dtype=dtype):
                cases = pd.Series([0, 1, 3, 6, 10, 15, 21, 28], index=index, dtype=dtype)

                original, smoothed = rt_covid19.prepare_cases(cases)

                self.assertEqual(original.index.tolist(), smoothed.index.tolist())
                self.assertGreater(len(smoothed), 0)
                self.assertTrue(np.isfinite(smoothed).all())

    def test_prepare_cases_rejects_non_finite_cumulative_values(self):
        index = pd.date_range("2020-01-01", periods=8)
        for non_finite in (np.nan, np.inf, -np.inf):
            with self.subTest(non_finite=non_finite):
                values = [0.0, 1.0, 3.0, non_finite, 5.0, 8.0, 12.0, 17.0]
                cases = pd.Series(values, index=index, dtype=float)
                with self.assertRaisesRegex(ValueError, "Cases must contain finite values"):
                    rt_covid19.prepare_cases(cases)

    def test_prepare_cases_rejects_negative_cumulative_values(self):
        index = pd.date_range("2020-01-01", periods=8)
        for values in (
            [-8, -7, -6, -5, -4, -3, -2, -1],
            [0, 1, 3, -1, 5, 8, 12, 17],
        ):
            with self.subTest(values=values):
                cases = pd.Series(values, index=index, dtype=float)
                with self.assertRaisesRegex(
                    ValueError,
                    "Cases must contain non-negative cumulative values",
                ):
                    rt_covid19.prepare_cases(cases)

    def test_prepare_cases_preserves_non_negative_downward_revisions(self):
        index = pd.date_range("2020-01-01", periods=8)
        cases = pd.Series([0, 2, 5, 4, 7, 11, 16, 22], index=index, dtype=float)

        original, smoothed = rt_covid19.prepare_cases(cases)

        self.assertIn(-1.0, original.tolist())
        self.assertEqual(original.index.tolist(), smoothed.index.tolist())

    def test_prepare_cases_rejects_ambiguous_indexes(self):
        for index in self.invalid_case_indexes():
            with self.subTest(index=index):
                cases = pd.Series([1.0, 2.0, 3.0], index=index)
                with self.assertRaisesRegex(
                    ValueError,
                    "Cases index must be one-dimensional, non-missing, unique, and increasing",
                ):
                    rt_covid19.prepare_cases(cases)

    def test_get_posteriors_normalizes_each_day(self):
        index = pd.date_range("2020-01-01", periods=4)
        cases = pd.Series([4.0, 5.0, 6.0, 7.0], index=index)

        posteriors, log_likelihood = rt_covid19.get_posteriors(
            cases, sigma=0.2, r_t_range=np.linspace(0, 4, 81)
        )

        np.testing.assert_allclose(posteriors.sum(axis=0).to_numpy(), 1.0)
        self.assertTrue(math.isfinite(log_likelihood))

    def test_get_posteriors_rejects_invalid_sigma(self):
        cases = pd.Series([1.0, 2.0])

        with self.assertRaisesRegex(ValueError, "Sigma"):
            rt_covid19.get_posteriors(cases, sigma=0)

    def test_get_posteriors_rejects_non_numeric_case_dtypes(self):
        invalid_values = (
            ["1", "2"],
            [True, False],
            np.array([1 + 1j, 2 + 2j]),
            pd.Categorical([1, 2]),
            pd.date_range("2020-01-01", periods=2),
        )

        for values in invalid_values:
            with self.subTest(dtype=pd.Series(values).dtype):
                with self.assertRaisesRegex(
                    ValueError,
                    "Smoothed cases must use a real numeric, non-boolean dtype",
                ):
                    rt_covid19.get_posteriors(pd.Series(values))

    def test_get_posteriors_accepts_numeric_case_dtypes(self):
        for dtype in (np.int64, np.float32):
            with self.subTest(dtype=dtype):
                cases = pd.Series([1, 2], dtype=dtype)

                posteriors, log_likelihood = rt_covid19.get_posteriors(
                    cases,
                    r_t_range=np.array([0.0, 1.0, 2.0]),
                )

                np.testing.assert_allclose(posteriors.sum(axis=0).to_numpy(), 1.0)
                self.assertTrue(math.isfinite(log_likelihood))

    def test_get_posteriors_rejects_ambiguous_indexes(self):
        for index in self.invalid_case_indexes():
            with self.subTest(index=index):
                cases = pd.Series([1.0, 2.0, 3.0], index=index)
                with self.assertRaisesRegex(
                    ValueError,
                    "Smoothed cases index must be one-dimensional, non-missing, unique, and increasing",
                ):
                    rt_covid19.get_posteriors(cases)

    def test_get_posteriors_rejects_invalid_rt_range(self):
        cases = pd.Series([1.0, 2.0])

        invalid_ranges = (
            (np.array([]), "non-empty, finite one-dimensional"),
            (np.array([[0.0, 1.0]]), "non-empty, finite one-dimensional"),
            (np.array([0.0, np.nan]), "non-empty, finite one-dimensional"),
            (np.array([0.0, np.inf]), "non-empty, finite one-dimensional"),
            (np.array([-0.1, 0.0, 0.1]), "non-negative and strictly increasing"),
            (np.array([0.0, 0.5, 0.5, 1.0]), "non-negative and strictly increasing"),
        )
        for r_t_range, message in invalid_ranges:
            with self.subTest(r_t_range=r_t_range):
                with self.assertRaisesRegex(ValueError, message):
                    rt_covid19.get_posteriors(cases, r_t_range=r_t_range)

    def test_highest_density_interval_excludes_low_mass_prefix(self):
        pmf = pd.Series([0.1, 0.6, 0.3], index=[0, 1, 2])

        interval = rt_covid19.highest_density_interval(pmf, p=0.8)
        frame_interval = rt_covid19.highest_density_interval(pd.DataFrame({"day": pmf}), p=0.8)

        self.assertEqual([1.0, 2.0], interval.tolist())
        self.assertEqual([1.0, 2.0], frame_interval.loc["day"].tolist())
        self.assertTrue(all(isinstance(value, (int, np.integer)) for value in interval))

    def test_highest_density_interval_validates_probability_type_and_range(self):
        pmf = pd.Series([0.1, 0.6, 0.3], index=[0.0, 1.0, 2.0])

        for probability in (0.8, np.float64(0.8)):
            with self.subTest(probability=probability):
                self.assertEqual(
                    [1.0, 2.0],
                    rt_covid19.highest_density_interval(pmf, p=probability).tolist(),
                )

        invalid_probabilities = (
            None,
            "0.8",
            0.8 + 0j,
            True,
            np.bool_(False),
            0.0,
            np.int64(0),
            1.0,
            np.nan,
            np.inf,
            -np.inf,
        )
        for probability in invalid_probabilities:
            with self.subTest(probability=probability):
                with self.assertRaisesRegex(
                    ValueError,
                    "finite real number strictly between zero and one",
                ):
                    rt_covid19.highest_density_interval(pmf, p=probability)

    def test_highest_density_interval_uses_numeric_grid_width(self):
        pmf = pd.Series([0.1, 0.4, 0.25, 0.25], index=[0, 100, 101, 102])

        interval = rt_covid19.highest_density_interval(pmf, p=0.5)

        self.assertEqual([100, 101], interval.tolist())

    def test_highest_density_interval_preserves_earliest_equal_width(self):
        pmf = pd.Series([0.25, 0.25, 0.25, 0.25], index=[0, 1, 2, 3])

        interval = rt_covid19.highest_density_interval(pmf, p=0.5)

        self.assertEqual([0, 1], interval.tolist())

    def test_highest_density_interval_preserves_valid_frame_column_order(self):
        pmf = pd.DataFrame(
            {
                "later": [0.1, 0.6, 0.3],
                "earlier": [0.7, 0.2, 0.1],
            },
            index=[0.0, 1.0, 2.0],
        )

        intervals = rt_covid19.highest_density_interval(pmf, p=0.8)

        self.assertEqual(["later", "earlier"], intervals.index.tolist())
        self.assertEqual([1.0, 2.0], intervals.loc["later"].tolist())
        self.assertEqual([0.0, 1.0], intervals.loc["earlier"].tolist())

    def test_highest_density_interval_rejects_empty_frames(self):
        empty_frames = (
            pd.DataFrame(),
            pd.DataFrame(index=[0.0, 1.0]),
            pd.DataFrame(columns=["day"]),
        )

        for pmf in empty_frames:
            with self.subTest(shape=pmf.shape):
                with self.assertRaisesRegex(ValueError, "must contain rows and columns"):
                    rt_covid19.highest_density_interval(pmf)

    def test_highest_density_interval_rejects_ambiguous_frame_columns(self):
        invalid_columns = (
            pd.Index(["day", "day"]),
            pd.Index(["day", None]),
            pd.MultiIndex.from_tuples([("day", 1), ("day", 2)]),
        )

        for columns in invalid_columns:
            with self.subTest(columns=columns):
                pmf = pd.DataFrame(
                    [[0.2, 0.2], [0.8, 0.8]],
                    index=[0.0, 1.0],
                    columns=columns,
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "columns must be one-dimensional, non-missing, and unique",
                ):
                    rt_covid19.highest_density_interval(pmf, p=0.8)

    def test_highest_density_interval_rejects_invalid_grid(self):
        invalid_indexes = (
            [0.0, 0.0, 1.0],
            [0.0, 2.0, 1.0],
            [0.0, np.nan, 2.0],
            [0.0, np.inf, 2.0],
            ["0", "1", "2"],
            [False, True, True],
            pd.MultiIndex.from_tuples([(0, 0), (1, 1), (2, 2)]),
        )

        for index in invalid_indexes:
            with self.subTest(index=index):
                pmf = pd.Series([0.1, 0.6, 0.3], index=index)
                with self.assertRaisesRegex(
                    ValueError, "HDI grid must be numeric, finite, and strictly increasing"
                ):
                    rt_covid19.highest_density_interval(pmf, p=0.8)

    @staticmethod
    def invalid_case_indexes():
        return (
            pd.Index([0, 0, 1]),
            pd.Index([2, 1, 0]),
            pd.DatetimeIndex(["2020-01-01", None, "2020-01-03"]),
            pd.MultiIndex.from_tuples([(0, 0), (1, 1), (2, 2)]),
        )


if __name__ == "__main__":
    unittest.main()
