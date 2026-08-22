"""MEDIAFOND market data source."""

from http_client import request

from . import utils


def mediafond(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """Fetch historical prices from MEDIAFOND."""
    response = request(
        "GET",
        "https://www.mediafond.it/grafici/tabella.php",
        params={"c": ticker},
        headers={
            "User-Agent": utils.BROWSER_USER_AGENT,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.mediafond.it/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        },
    )
    market_data = [
        {
            "date": utils.convert_italian_date(item["data"]),
            "marketPrice": float(item["valore"].replace(",", ".")),
        }
        for item in response.json()
    ]

    return utils.fill_missing_dates(market_data, start_date, end_date)
