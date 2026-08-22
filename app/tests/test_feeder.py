"""Tests for the feeder orchestration."""

import unittest
from unittest.mock import MagicMock, patch

from ghostfolio_feeder import ghostfolio_feeder, get_market_data


class FeederTest(unittest.TestCase):
    """Verify profile creation and incremental updates."""

    @patch.dict(
        "ghostfolio_feeder.data_source_mapping",
        {"test": MagicMock(return_value=[{"date": "2026-01-01", "marketPrice": 1.0}])},
    )
    def test_creates_missing_profile_and_populates_prices(self):
        client = MagicMock()
        client.get_asset_profile.return_value = {
            "assetProfile": {},
            "marketData": [],
        }
        profile = {"name": "Test"}
        source = {
            "name": "test",
            "ticker": "TEST",
            "start_date": "2026-01-01",
            "end_date": "2026-01-02",
        }

        ghostfolio_feeder(client, "GF_TEST", profile, source)

        client.create_profile_data.assert_called_once_with("GF_TEST")
        client.set_profile_data.assert_called_once_with("GF_TEST", profile)
        client.populate_market_data.assert_called_once_with(
            "GF_TEST",
            {"marketData": [{"date": "2026-01-01", "marketPrice": 1.0}]},
        )

    def test_rejects_invalid_symbol_only_when_profile_is_missing(self):
        client = MagicMock()
        client.get_asset_profile.return_value = {
            "assetProfile": {},
            "marketData": [],
        }

        with self.assertRaisesRegex(ValueError, "must start with 'GF_'"):
            ghostfolio_feeder(
                client,
                "LEGACY-SYMBOL",
                {},
                {"name": "local", "ticker": "unused"},
            )

        client.create_profile_data.assert_not_called()

    def test_uses_latest_date_even_when_api_data_is_unsorted(self):
        client = MagicMock()
        client.get_asset_profile.return_value = {
            "assetProfile": {"symbol": "TEST"},
            "marketData": [
                {"date": "2026-07-01T00:00:00.000Z", "marketPrice": 2.0},
                {"date": "2026-01-01T00:00:00.000Z", "marketPrice": 1.0},
            ],
        }
        source_function = MagicMock(
            return_value=[{"date": "2026-04-02", "marketPrice": 1.5}]
        )
        source = {"name": "test", "ticker": "TEST", "start_date": "2020-01-01"}

        with patch.dict(
            "ghostfolio_feeder.data_source_mapping",
            {"test": source_function},
        ):
            ghostfolio_feeder(client, "TEST", {}, source)

        source_function.assert_called_once_with("TEST", "2026-04-02", None)
        client.create_profile_data.assert_not_called()

    def test_rejects_unknown_source(self):
        with self.assertRaisesRegex(ValueError, "Unsupported data source"):
            get_market_data({"name": "missing", "ticker": "TEST"})


if __name__ == "__main__":
    unittest.main()
