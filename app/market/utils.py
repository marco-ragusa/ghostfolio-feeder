"""Shared market data helpers."""

from datetime import date, timedelta


ITALIAN_MONTHS = (
    "Gen",
    "Feb",
    "Mar",
    "Apr",
    "Mag",
    "Giu",
    "Lug",
    "Ago",
    "Set",
    "Ott",
    "Nov",
    "Dic",
)

BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/151.0.0.0 Safari/537.36"
)


def convert_italian_date(date_str: str) -> str | None:
    """Convert an Italian month and year to ``YYYY-MM-01``."""
    parts = date_str.split()
    if len(parts) != 2:
        return None

    if parts[1].isdigit():
        month_str, year_str = parts[0][:3].capitalize(), parts[1]
    elif parts[0].isdigit():
        month_str, year_str = parts[1][:3].capitalize(), parts[0]
    else:
        return None

    if month_str not in ITALIAN_MONTHS:
        return None

    month_number = ITALIAN_MONTHS.index(month_str) + 1
    return f"{year_str}-{month_number:02d}-01"


def fill_missing_dates(
    data_list: list,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list:
    """Normalize prices and forward-fill missing calendar days."""
    if not data_list:
        return []

    end_date = end_date or date.today().isoformat()
    if start_date and start_date > end_date:
        raise ValueError("start_date must not be after end_date")

    prices_by_date = {
        str(item["date"]): float(item["marketPrice"]) for item in data_list
    }
    normalized = [
        {"date": item_date, "marketPrice": market_price}
        for item_date, market_price in sorted(prices_by_date.items())
        if item_date <= end_date
    ]

    if start_date:
        previous = next(
            (item for item in reversed(normalized) if item["date"] <= start_date),
            None,
        )
        normalized = [item for item in normalized if item["date"] >= start_date]
        if previous and (not normalized or normalized[0]["date"] > start_date):
            normalized.insert(
                0,
                {"date": start_date, "marketPrice": previous["marketPrice"]},
            )

    if not normalized:
        return []

    if end_date > normalized[-1]["date"]:
        normalized.append(
            {"date": end_date, "marketPrice": normalized[-1]["marketPrice"]}
        )

    filled = [normalized[0]]
    for item in normalized[1:]:
        current_date = date.fromisoformat(filled[-1]["date"]) + timedelta(days=1)
        item_date = date.fromisoformat(item["date"])
        while current_date < item_date:
            filled.append(
                {
                    "date": current_date.isoformat(),
                    "marketPrice": filled[-1]["marketPrice"],
                }
            )
            current_date += timedelta(days=1)
        filled.append(item)

    return filled
