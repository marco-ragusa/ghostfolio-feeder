"""Feed external market data into Ghostfolio."""

from datetime import date, timedelta

from ghostfolio import Ghostfolio
from market import data_source_mapping


def subtract_days_from_date(input_date: str, days_to_subtract: int = 0) -> str:
    """Subtract days from an ISO date."""
    return (
        date.fromisoformat(input_date) - timedelta(days=days_to_subtract)
    ).isoformat()


def get_market_data(data_source: dict, start_date: str | None = None) -> dict:
    """Retrieve and format data from a configured market source."""
    source_name = data_source["name"]
    source = data_source_mapping.get(source_name)

    if source is None:
        supported = ", ".join(sorted(data_source_mapping))
        raise ValueError(
            f"Unsupported data source '{source_name}'. Supported sources: {supported}"
        )

    market_data = source(
        data_source["ticker"],
        start_date if start_date is not None else data_source.get("start_date"),
        data_source.get("end_date"),
    )

    if not market_data:
        raise ValueError(f"No market data returned by '{source_name}'")

    return {"marketData": market_data}


def ghostfolio_feeder(
    ghostfolio: Ghostfolio,
    symbol: str,
    profile_data: dict,
    data_source: dict,
) -> None:
    """Create a profile when needed and upsert its market data."""
    details = ghostfolio.get_asset_profile(symbol)

    if not details.get("assetProfile"):
        if not symbol.startswith("GF_"):
            raise ValueError(
                f"Cannot create '{symbol}': new MANUAL symbols must start with 'GF_'"
            )
        ghostfolio.create_profile_data(symbol)
        ghostfolio.set_profile_data(symbol, profile_data)

    start_date = data_source.get("start_date")
    existing_market_data = details.get("marketData") or []

    if existing_market_data:
        last_item = max(existing_market_data, key=lambda item: item["date"])
        last_date = last_item["date"].split("T")[0]
        start_date = subtract_days_from_date(last_date, 90)

    ghostfolio.populate_market_data(
        symbol,
        get_market_data(data_source, start_date=start_date),
    )
