"""Client for the Ghostfolio API."""

from urllib.parse import quote

from http_client import request


class Ghostfolio:
    """Manage MANUAL asset profiles and market data in Ghostfolio."""

    def __init__(self, host: str, access_token: str) -> None:
        self.host = host.rstrip("/")
        self.auth_token = self._get_auth_token(access_token)

    @property
    def headers(self) -> dict:
        """Return the authorization header."""
        return {"Authorization": f"Bearer {self.auth_token}"}

    def _get_auth_token(self, access_token: str) -> str:
        response = request(
            "POST",
            f"{self.host}/api/v1/auth/anonymous",
            json={"accessToken": access_token},
        )
        return response.json()["authToken"]

    def _url(self, endpoint: str, symbol: str) -> str:
        encoded_symbol = quote(symbol, safe="")
        return f"{self.host}/api/v1/{endpoint}/MANUAL/{encoded_symbol}"

    def get_asset_profile(self, symbol: str) -> dict:
        """Return the asset profile and its market data.

        Ghostfolio returns 404 when a MANUAL symbol has not been created yet.
        """
        response = request(
            "GET",
            self._url("asset-profiles", symbol),
            headers=self.headers,
            allowed_statuses=(404,),
        )

        if response.status_code == 404:
            return {"assetProfile": {}, "marketData": []}

        return response.json()

    def create_profile_data(self, symbol: str) -> dict:
        """Create a MANUAL asset profile."""
        response = request(
            "POST",
            self._url("admin/profile-data", symbol),
            headers=self.headers,
        )
        return response.json()

    def set_profile_data(self, symbol: str, profile_data: dict) -> dict:
        """Update a MANUAL asset profile."""
        response = request(
            "PATCH",
            self._url("admin/profile-data", symbol),
            headers=self.headers,
            json=profile_data,
        )
        return response.json()

    def populate_market_data(self, symbol: str, market_data: dict) -> int:
        """Upsert market data for a MANUAL asset profile."""
        response = request(
            "POST",
            self._url("market-data", symbol),
            headers=self.headers,
            json=market_data,
        )
        return response.status_code

    def delete_profile_data(self, symbol: str) -> int:
        """Delete a MANUAL asset profile."""
        response = request(
            "DELETE",
            self._url("admin/profile-data", symbol),
            headers=self.headers,
            allowed_statuses=(404,),
        )
        return response.status_code
