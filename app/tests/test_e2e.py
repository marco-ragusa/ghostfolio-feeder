"""End-to-end test against a real Ghostfolio instance."""

import os
import unittest
from pathlib import Path

from ghostfolio import Ghostfolio
from ghostfolio_feeder import ghostfolio_feeder
from http_client import request


HOST = os.getenv("GHOSTFOLIO_E2E_HOST")


@unittest.skipUnless(HOST, "set GHOSTFOLIO_E2E_HOST to run the E2E test")
class GhostfolioE2ETest(unittest.TestCase):
    """Create, populate, read, and delete a MANUAL asset profile."""

    @classmethod
    def setUpClass(cls):
        signup = request("POST", f"{HOST}/api/v1/user").json()
        if signup.get("role") != "ADMIN":
            raise RuntimeError("E2E requires a fresh Ghostfolio database")
        cls.client = Ghostfolio(HOST, signup["accessToken"])

    def test_feeds_local_data(self):
        symbol = "GF_GHOSTFOLIO_FEEDER_E2E"
        profile = {
            "assetClass": "EQUITY",
            "assetSubClass": "MUTUALFUND",
            "comment": "Created by the Ghostfolio Feeder E2E test",
            "currency": "EUR",
            "name": "Ghostfolio Feeder E2E",
            "symbolMapping": {},
        }
        source_file = Path(__file__).parents[1] / "data" / "local" / "example.json"
        source = {
            "name": "local",
            "ticker": str(source_file),
            "start_date": "2024-01-01",
            "end_date": "2024-01-03",
        }

        try:
            ghostfolio_feeder(self.client, symbol, profile, source)
            details = self.client.get_asset_profile(symbol)

            self.assertEqual(details["assetProfile"]["name"], profile["name"])
            self.assertEqual(len(details["marketData"]), 3)
            self.assertEqual(
                details["marketData"][-1]["marketPrice"],
                104,
            )
        finally:
            self.client.delete_profile_data(symbol)


if __name__ == "__main__":
    unittest.main()
