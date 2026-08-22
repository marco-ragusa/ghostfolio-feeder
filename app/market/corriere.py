"""Corriere Borsa market data source."""

import json
from datetime import datetime, timezone

from http_client import request

from . import utils


URL = "https://borsa.corriere.it/ajax/getchartdata/"


def corriere(
    ticker: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list:
    """Fetch historical prices using a current Corriere chart code."""
    response = request(
        "GET",
        URL,
        params={"code": ticker, "periodType": 1},
        headers={
            "User-Agent": utils.BROWSER_USER_AGENT,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://borsa.corriere.it/fondi-etf/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        },
    )
    payload = response.json()

    if not payload:
        return []

    # Corriere returns JSON encoded inside a JSON string.
    if isinstance(payload, str):
        payload = json.loads(payload)

    historical_data = json.loads(payload.get("historicalData") or "[]")
    market_data = [
        {
            "date": datetime.fromtimestamp(
                item[0] / 1000,
                timezone.utc,
            )
            .date()
            .isoformat(),
            "marketPrice": item[1],
        }
        for item in historical_data
    ]

    return utils.fill_missing_dates(market_data, start_date, end_date)
