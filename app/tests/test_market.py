"""Tests for market adapters and normalization."""

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from market.boerse_frankfurt import boerse_frankfurt
from market.corriere import corriere
from market.local import local
from market.utils import fill_missing_dates


def json_response(payload):
    result = MagicMock()
    result.json.return_value = payload
    return result


class MarketTest(unittest.TestCase):
    """Exercise the shared normalization and repaired sources."""

    def test_profile_example_uses_current_manual_symbols(self):
        profile_file = Path(__file__).parents[1] / "data" / "profiles.json.example"
        profiles = json.loads(profile_file.read_text(encoding="utf-8"))

        self.assertTrue(
            all(profile["symbol"].startswith("GF_") for profile in profiles)
        )
        self.assertEqual(profiles[0]["symbol"], "GF_21BC_DE")
        allianz = next(
            profile for profile in profiles if profile["symbol"] == "GF_ALL_IN_AZN"
        )
        self.assertEqual(
            allianz["profile_data"]["name"],
            "Allianz Insieme Linea Azionaria",
        )
        self.assertEqual(allianz["data_source"]["ticker"], "FC.ALPFRA12")

    def test_empty_source_stays_empty(self):
        self.assertEqual(fill_missing_dates([]), [])

    def test_csv_prices_are_numbers(self):
        csv_file = Path(__file__).parents[1] / "data" / "local" / "example.csv"
        rows = local(
            str(csv_file),
            start_date="2020-01-01",
            end_date="2020-01-02",
        )

        self.assertEqual(rows[0]["marketPrice"], 100.0)
        self.assertIsInstance(rows[0]["marketPrice"], float)

    def test_duplicate_dates_keep_latest_value(self):
        rows = fill_missing_dates(
            [
                {"date": "2026-01-01", "marketPrice": 1},
                {"date": "2026-01-01", "marketPrice": 2},
            ],
            start_date="2026-01-01",
            end_date="2026-01-01",
        )

        self.assertEqual(rows, [{"date": "2026-01-01", "marketPrice": 2.0}])

    def test_ignores_values_after_requested_end_date(self):
        rows = fill_missing_dates(
            [
                {"date": "2026-01-01", "marketPrice": 1},
                {"date": "2030-01-01", "marketPrice": 2},
            ],
            start_date="2026-01-01",
            end_date="2026-01-02",
        )

        self.assertEqual(
            rows,
            [
                {"date": "2026-01-01", "marketPrice": 1.0},
                {"date": "2026-01-02", "marketPrice": 1.0},
            ],
        )

    @patch("market.boerse_frankfurt.request")
    def test_boerse_frankfurt_uses_current_api(self, http_request):
        timestamp = int(datetime(2026, 8, 21, tzinfo=timezone.utc).timestamp())
        http_request.return_value = json_response(
            {"s": "ok", "t": [timestamp], "c": [15.79]}
        )

        rows = boerse_frankfurt(
            "XETR:CH1199067674",
            start_date="2026-08-21",
            end_date="2026-08-21",
        )

        self.assertEqual(
            rows,
            [{"date": "2026-08-21", "marketPrice": 15.79}],
        )
        self.assertEqual(
            http_request.call_args.kwargs["params"]["symbol"],
            "XETR:CH1199067674",
        )
        headers = http_request.call_args.kwargs["headers"]
        self.assertIn("Mozilla/5.0", headers["User-Agent"])
        self.assertEqual(
            headers["Referer"],
            "https://live.deutsche-boerse.com/",
        )

    @patch("market.corriere.request")
    def test_corriere_uses_current_chart_api(self, http_request):
        timestamp_ms = int(
            datetime(2026, 8, 21, tzinfo=timezone.utc).timestamp() * 1000
        )
        body = {"historicalData": json.dumps([[timestamp_ms, 52701.58]])}
        http_request.return_value = json_response(json.dumps(body))

        rows = corriere(
            "CB.FTSEMIB",
            start_date="2026-08-21",
            end_date="2026-08-21",
        )

        self.assertEqual(
            rows,
            [{"date": "2026-08-21", "marketPrice": 52701.58}],
        )
        headers = http_request.call_args.kwargs["headers"]
        self.assertIn("Mozilla/5.0", headers["User-Agent"])
        self.assertEqual(
            headers["Referer"],
            "https://borsa.corriere.it/fondi-etf/",
        )


if __name__ == "__main__":
    unittest.main()
