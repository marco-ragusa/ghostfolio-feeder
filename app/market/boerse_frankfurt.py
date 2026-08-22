"""Börse Frankfurt market data source."""

from datetime import date, datetime, time, timezone

from http_client import request

from . import utils


URL = "https://api.live.deutsche-boerse.com/v1/tradingview/history"


def _timestamp(value: str | None, *, end_of_day: bool = False) -> int:
    day = date.fromisoformat(value) if value else date.today()
    clock = time.max if end_of_day else time.min
    return int(datetime.combine(day, clock, tzinfo=timezone.utc).timestamp())


def boerse_frankfurt(
    ticker: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list:
    """Fetch daily closing prices from Börse Frankfurt.

    ``ticker`` uses the ``MIC:ISIN`` format, for example
    ``XETR:CH1199067674``.
    """
    response = request(
        "GET",
        URL,
        headers={
            "User-Agent": utils.BROWSER_USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
            "Origin": "https://live.deutsche-boerse.com",
            "Referer": "https://live.deutsche-boerse.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        },
        params={
            "symbol": ticker,
            "resolution": "1D",
            "from": _timestamp(start_date or "1970-01-01"),
            "to": _timestamp(end_date, end_of_day=True),
        },
    )
    payload = response.json()

    if payload.get("s") != "ok":
        return []

    timestamps = payload.get("t", [])
    closing_prices = payload.get("c", [])
    if len(timestamps) != len(closing_prices):
        raise ValueError("Invalid Börse Frankfurt response")

    market_data = [
        {
            "date": datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat(),
            "marketPrice": price,
        }
        for timestamp, price in zip(timestamps, closing_prices)
    ]

    return utils.fill_missing_dates(market_data, start_date, end_date)
