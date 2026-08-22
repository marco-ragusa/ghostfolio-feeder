"""Local CSV and JSON market data source."""

import csv
import json

from . import utils


def local(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """Read prices from a local JSON or CSV file."""
    suffix = ticker.lower()
    if not suffix.endswith((".json", ".csv")):
        raise ValueError("File format not supported. Only use JSON or CSV.")

    with open(ticker, encoding="utf-8", newline="") as file:
        if suffix.endswith(".json"):
            market_data = json.load(file)
        else:
            market_data = list(csv.DictReader(file))

    return utils.fill_missing_dates(market_data, start_date, end_date)
