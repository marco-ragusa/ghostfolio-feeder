"""Tests for the Ghostfolio API client endpoint fallback behavior."""
import unittest
from unittest.mock import MagicMock, patch

from ghostfolio import Ghostfolio


HOST = 'https://ghostfolio.example.com'
SYMBOL = 'TEST.SYM'
NEW_URL = f'{HOST}/api/v1/asset-profiles/MANUAL/{SYMBOL}'
OLD_URL = f'{HOST}/api/v1/market-data/MANUAL/{SYMBOL}'

MARKET_DATA = [
    {'date': '2026-07-01T00:00:00.000Z', 'marketPrice': 1.23},
    {'date': '2026-07-02T00:00:00.000Z', 'marketPrice': 1.24},
]
ASSET_PROFILE = {'symbol': SYMBOL, 'currency': 'AUD', 'name': 'Test Fund'}
DETAILS_BODY = {'assetProfile': ASSET_PROFILE, 'marketData': MARKET_DATA}


def make_response(status_code=200, json_body=None):
    """Build a mock requests response."""
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_body if json_body is not None else {}
    return response


class GhostfolioEndpointTest(unittest.TestCase):
    """Exercise new-endpoint-first, old-endpoint-fallback behavior."""

    def setUp(self):
        Ghostfolio._endpoint_cache = {}
        patcher = patch('ghostfolio.ghostfolio.requests')
        self.requests = patcher.start()
        self.addCleanup(patcher.stop)
        self.requests.post.return_value = make_response(
            200, {'authToken': 'jwt-token'}
        )

    def make_client(self, get_responses):
        """Create a Ghostfolio client with scripted GET responses."""
        self.requests.get.side_effect = get_responses
        return Ghostfolio(HOST, 'access-token', SYMBOL)

    def get_urls(self):
        """Return the list of URLs passed to requests.get."""
        return [call.args[0] for call in self.requests.get.call_args_list]

    def test_uses_asset_profiles_endpoint_when_available(self):
        client = self.make_client([make_response(200, DETAILS_BODY)])

        self.assertEqual(client.market_data, MARKET_DATA)
        self.assertEqual(self.get_urls(), [NEW_URL])

    def test_falls_back_to_market_data_endpoint_on_404(self):
        client = self.make_client([
            make_response(404, {'statusCode': 404}),
            make_response(200, DETAILS_BODY),
        ])

        self.assertEqual(client.market_data, MARKET_DATA)
        self.assertEqual(self.get_urls(), [NEW_URL, OLD_URL])

    def test_returns_empty_when_both_endpoints_404(self):
        client = self.make_client([
            make_response(404, {'statusCode': 404}),
            make_response(404, {'statusCode': 404}),
        ])

        self.assertEqual(client.market_data, [])
        self.assertEqual(self.get_urls(), [NEW_URL, OLD_URL])

    def test_remembers_working_endpoint_after_fallback(self):
        client = self.make_client([
            make_response(404, {'statusCode': 404}),
            make_response(200, DETAILS_BODY),
            make_response(200, DETAILS_BODY),
        ])
        client.update_market_data()

        self.assertEqual(self.get_urls(), [NEW_URL, OLD_URL, OLD_URL])

    def test_remembers_new_endpoint_after_success(self):
        client = self.make_client([
            make_response(200, DETAILS_BODY),
            make_response(200, DETAILS_BODY),
        ])
        client.update_market_data()

        self.assertEqual(self.get_urls(), [NEW_URL, NEW_URL])

    def test_does_not_cache_endpoint_when_both_404(self):
        client = self.make_client([
            make_response(404, {'statusCode': 404}),
            make_response(404, {'statusCode': 404}),
            make_response(200, DETAILS_BODY),
        ])
        client.update_market_data()

        self.assertEqual(client.market_data, MARKET_DATA)
        self.assertEqual(self.get_urls(), [NEW_URL, OLD_URL, NEW_URL])

    def test_get_profile_data_returns_asset_profile(self):
        client = self.make_client([
            make_response(200, DETAILS_BODY),
            make_response(200, DETAILS_BODY),
        ])

        self.assertEqual(client.get_profile_data(), ASSET_PROFILE)

    def test_get_profile_data_empty_when_symbol_missing(self):
        client = self.make_client([
            make_response(404, {'statusCode': 404}),
            make_response(404, {'statusCode': 404}),
            make_response(404, {'statusCode': 404}),
            make_response(404, {'statusCode': 404}),
        ])

        self.assertEqual(client.get_profile_data(), {})


if __name__ == '__main__':
    unittest.main()
