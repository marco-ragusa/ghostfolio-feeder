"""Fon.Te. market data source."""

from bs4 import BeautifulSoup
from http_client import request

from . import utils


def fondofonte_scraper(html: str) -> list:
    """Extract monthly prices from a Fon.Te. page."""
    market_data = []
    soup = BeautifulSoup(html, "html.parser")
    for toggle in soup.find_all(class_="toggle-acf"):
        title = toggle.find("a")
        content = toggle.find_next(class_="toggle-content-acf")
        if not title or not content:
            continue

        for row in content.find_all(class_="toggle_element_row"):
            cells = row.find_all("span", {"class": None})
            if len(cells) < 2:
                continue
            period = cells[0].get_text(strip=True)
            if period == "Periodo":
                continue
            market_data.append(
                {
                    "date": f"{period} {title.get_text(strip=True)}",
                    "marketPrice": cells[1].get_text(strip=True),
                }
            )

    return market_data


def fondofonte(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """Fetch historical prices from Fon.Te."""
    url = (
        "https://www.fondofonte.it/gestione-finanziaria/"
        f"i-valori-quota-dei-comparti/{ticker}/"
    )
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
            "date": utils.convert_italian_date(item["date"]),
            "marketPrice": float(item["marketPrice"].replace(",", ".")),
        }
        for item in fondofonte_scraper(response.text)
    ]

    return utils.fill_missing_dates(market_data, start_date, end_date)
