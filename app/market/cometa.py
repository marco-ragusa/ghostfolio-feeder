"""Cometa market data source."""

import re
from datetime import datetime

from bs4 import BeautifulSoup
from http_client import request

from . import utils


def cometa_scraper(html: str) -> list:
    """Extract monthly prices from a Cometa page."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="table_2")
    if not table or not table.has_attr("data-wpdatatable_id"):
        raise ValueError("Cometa price table not found")

    table_id = table["data-wpdatatable_id"]
    id_pattern = re.compile(rf"^table_{table_id}_row_\d+$")
    rows = soup.find_all("tr", id=id_pattern, attrs={"data-row-index": True})
    market_data = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            market_data.append(
                {
                    "date": cells[0].get_text(strip=True),
                    "marketPrice": cells[1].get_text(strip=True),
                }
            )

    return market_data


def cometa(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """Fetch historical prices from Cometa."""
    url = f"https://www.cometafondo.it/quota/{ticker}/"
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
            "date": datetime.strptime(item["date"], "%m/%Y").date().isoformat(),
            "marketPrice": float(item["marketPrice"].replace(",", ".")),
        }
        for item in cometa_scraper(response.text)
    ]

    return utils.fill_missing_dates(market_data, start_date, end_date)
