"""Ghostfolio module."""
import requests


class Ghostfolio:
    """A class to interact with the Ghostfolio API for managing market and profile data."""

    # Ghostfolio 3.13.0 moved GET api/v1/market-data/:dataSource/:symbol to
    # GET api/v1/asset-profiles/:dataSource/:symbol. The version is not
    # discoverable without admin parsing, so probe the new endpoint first and
    # fall back to the old one. Remembers the working endpoint per host.
    _endpoint_cache = {}

    def __init__(self, host, access_token, symbol) -> None:
        """Initialize the Ghostfolio instance with host, access_token, and symbol."""
        self.host = host
        self.access_token = access_token
        self.symbol = symbol
        self.auth_token = self.get_auth_token()
        self.market_data = []

        self.update_market_data()


    def get_headers(self) -> dict:
        """Return the headers required for making authorized API requests."""
        return {
            'Authorization': f'Bearer {self.auth_token}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }


    def get_auth_token(self) -> str:
        """Retrieve the authentication token from the API using the access token."""
        headers = {
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        json_data = {
            'accessToken': self.access_token,
        }

        response = requests.post(
            f'{self.host}/api/v1/auth/anonymous',
            headers=headers,
            json=json_data,
            verify=False,
            timeout=10,
        )
        return response.json()['authToken']


    def create_profile_data(self) -> dict:
        """Create a new profile data entry for the specified symbol."""
        headers = self.get_headers()

        response = requests.post(
            f'{self.host}/api/v1/admin/profile-data/MANUAL/{self.symbol}',
            headers=headers,
            verify=False,
            timeout=10,
        )
        return response.json()


    def set_profile_data(self, profile_data) -> dict:
        """Set the profile data for the specified symbol."""
        headers = self.get_headers()

        response = requests.patch(
            f'{self.host}/api/v1/admin/profile-data/MANUAL/{self.symbol}',
            headers=headers,
            json=profile_data,
            verify=False,
            timeout=10,
        )
        return response.json()


    def get_market_data_details(self) -> dict:
        """Retrieve the asset profile and market data for the specified symbol.

        Both endpoints return the same {assetProfile, marketData} shape. A 404
        from the new endpoint means either an old Ghostfolio version or a
        symbol that does not exist yet, so only a successful response decides
        which endpoint the host supports.
        """
        headers = self.get_headers()
        urls = {
            'asset-profiles': f'{self.host}/api/v1/asset-profiles/MANUAL/{self.symbol}',
            'market-data': f'{self.host}/api/v1/market-data/MANUAL/{self.symbol}',
        }

        cached_endpoint = Ghostfolio._endpoint_cache.get(self.host)
        endpoints = [cached_endpoint] if cached_endpoint else ['asset-profiles', 'market-data']

        for endpoint in endpoints:
            response = requests.get(
                urls[endpoint],
                headers=headers,
                verify=False,
                timeout=10,
            )
            if response.status_code == 404:
                continue

            Ghostfolio._endpoint_cache[self.host] = endpoint
            return response.json()

        return {'assetProfile': {}, 'marketData': []}


    def get_market_data(self) -> list:
        """Retrieve the market data for the specified symbol."""
        return self.get_market_data_details().get('marketData') or []


    def get_profile_data(self) -> dict:
        """Retrieve the profile data for the specified symbol."""
        return self.get_market_data_details().get('assetProfile') or {}


    def profile_data_is_exist(self) -> bool:
        """Check if profile data exists for the specified symbol."""
        profile_data = self.get_market_data()

        result = False
        if profile_data:
            result = True

        return result


    def update_market_data(self) -> None:
        """Update the market data for the specified symbol."""
        # Fetch market_data
        self.market_data = self.get_market_data()
        if not self.market_data:
            self.market_data = []


    def populate_market_data(self, market_data) -> int:
        """Populate the market data with new entries for the specified symbol."""
        headers = self.get_headers()

        response = requests.post(
            f'{self.host}/api/v1/market-data/MANUAL/{self.symbol}',
            headers=headers,
            json=market_data,
            verify=False,
            timeout=10,
        )

        self.update_market_data()

        return response.status_code


    def market_data_is_exist(self) -> bool:
        """Check if market data exists for the specified symbol."""
        result = False
        if self.market_data:
            result = True

        return result


    def get_last_market_data(self) -> dict:
        """Retrieve the last entry from the market data."""
        return self.market_data[-1]


    def delete_profile_data(self) -> int:
        """Delete the profile data for the specified symbol."""
        headers = self.get_headers()

        response = requests.delete(
            f'{self.host}/api/v1/admin/profile-data/MANUAL/{self.symbol}',
            headers=headers,
            verify=False,
            timeout=10,
        )

        return response.status_code
