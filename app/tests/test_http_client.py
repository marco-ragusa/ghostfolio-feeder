"""Tests for the shared HTTP defaults."""

import unittest
from unittest.mock import MagicMock, patch

from http_client import DEFAULT_TIMEOUT, request


class HttpClientTest(unittest.TestCase):
    """Verify timeout and expected-status handling."""

    @patch("http_client._session")
    def test_uses_default_timeout_and_raises_for_errors(self, session):
        response = MagicMock(status_code=500)
        session.request.return_value = response

        request("GET", "https://example.com")

        session.request.assert_called_once_with(
            "GET",
            "https://example.com",
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("http_client._session")
    def test_allows_an_expected_status(self, session):
        response = MagicMock(status_code=404)
        session.request.return_value = response

        request(
            "GET",
            "https://example.com/missing",
            allowed_statuses=(404,),
            timeout=1,
        )

        response.raise_for_status.assert_not_called()
        session.request.assert_called_once_with(
            "GET",
            "https://example.com/missing",
            timeout=1,
        )


if __name__ == "__main__":
    unittest.main()
