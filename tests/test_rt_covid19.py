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


if __name__ == "__main__":
    unittest.main()
