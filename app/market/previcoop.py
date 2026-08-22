"""Previdenza Cooperativa market data source."""

from datetime import datetime

from bs4 import BeautifulSoup
from http_client import request

from . import utils


def previcoop_scraper(html: str) -> list:
    """Extract prices from a Previdenza Cooperativa page."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="table_4")
    if not table:
        raise ValueError("Previdenza Cooperativa price table not found")

    market_data = []
    for row in table.select("tbody tr"):
        cells = row.find_all("td")
        if len(cells) == 3:
            market_data.append(
                {
                    "date": cells[0].get_text(strip=True),
                    "marketPrice": cells[1].get_text(strip=True),
                }
            )

    return market_data


def previcoop(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """Fetch historical prices from Previdenza Cooperativa."""
    url = f"https://www.previdenzacooperativa.it/{ticker}/"
    response = request(
        "GET",
        url,
        headers={
            "User-Agent": utils.BROWSER_USER_AGENT,
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
            "Referer": url,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        },
    )
    market_data = [
        {
            "date": datetime.strptime(item["date"], "%d/%m/%Y").date().isoformat(),
            "marketPrice": float(item["marketPrice"].replace(",", ".")),
        }
        for item in previcoop_scraper(response.text)
    ]

    return utils.fill_missing_dates(market_data, start_date, end_date)
