"""Tests for the Ghostfolio API client."""

import unittest
from unittest.mock import MagicMock, call, patch

from ghostfolio import Ghostfolio


HOST = "https://ghostfolio.example.com"
SYMBOL = "TEST/SYM"
ENCODED_SYMBOL = "TEST%2FSYM"


def response(status_code=200, json_body=None):
    """Build a small requests response mock."""
    result = MagicMock()
    result.status_code = status_code
    result.json.return_value = json_body if json_body is not None else {}
    return result


class GhostfolioTest(unittest.TestCase):
    """Exercise the endpoints used by the feeder."""

    def setUp(self):
        patcher = patch("ghostfolio.ghostfolio.request")
        self.request = patcher.start()
        self.addCleanup(patcher.stop)
        self.request.return_value = response(200, {"authToken": "jwt-token"})
        self.client = Ghostfolio(f"{HOST}/", "access-token")
        self.request.reset_mock()

    def test_authenticates_with_access_token(self):
        self.request.return_value = response(200, {"authToken": "new-token"})

        client = Ghostfolio(HOST, "secret")

        self.assertEqual(client.auth_token, "new-token")
        self.request.assert_called_once_with(
            "POST",
            f"{HOST}/api/v1/auth/anonymous",
            json={"accessToken": "secret"},
        )

    def test_reads_current_asset_profiles_endpoint(self):
        details = {"assetProfile": {"symbol": SYMBOL}, "marketData": []}
        self.request.return_value = response(200, details)

        self.assertEqual(self.client.get_asset_profile(SYMBOL), details)
        self.request.assert_called_once_with(
            "GET",
            f"{HOST}/api/v1/asset-profiles/MANUAL/{ENCODED_SYMBOL}",
            headers={"Authorization": "Bearer jwt-token"},
            allowed_statuses=(404,),
        )

    def test_returns_empty_details_for_missing_symbol(self):
        self.request.return_value = response(404)

        self.assertEqual(
            self.client.get_asset_profile(SYMBOL),
            {"assetProfile": {}, "marketData": []},
        )

    def test_writes_profile_and_market_data_to_current_endpoints(self):
        self.request.side_effect = [response(), response(), response(201)]
        profile = {"name": "Test"}
        prices = {"marketData": [{"date": "2026-01-01", "marketPrice": 1.0}]}

        self.client.create_profile_data(SYMBOL)
        self.client.set_profile_data(SYMBOL, profile)
        status = self.client.populate_market_data(SYMBOL, prices)

        self.assertEqual(status, 201)
        self.assertEqual(
            self.request.call_args_list,
            [
                call(
                    "POST",
                    f"{HOST}/api/v1/admin/profile-data/MANUAL/{ENCODED_SYMBOL}",
                    headers={"Authorization": "Bearer jwt-token"},
                ),
                call(
                    "PATCH",
                    f"{HOST}/api/v1/admin/profile-data/MANUAL/{ENCODED_SYMBOL}",
                    headers={"Authorization": "Bearer jwt-token"},
                    json=profile,
                ),
                call(
                    "POST",
                    f"{HOST}/api/v1/market-data/MANUAL/{ENCODED_SYMBOL}",
                    headers={"Authorization": "Bearer jwt-token"},
                    json=prices,
                ),
            ],
        )

    def test_delete_is_idempotent_for_missing_profile(self):
        self.request.return_value = response(404)

        status = self.client.delete_profile_data(SYMBOL)

        self.assertEqual(status, 404)
        self.request.assert_called_once_with(
            "DELETE",
            f"{HOST}/api/v1/admin/profile-data/MANUAL/{ENCODED_SYMBOL}",
            headers={"Authorization": "Bearer jwt-token"},
            allowed_statuses=(404,),
        )


if __name__ == "__main__":
    unittest.main()
