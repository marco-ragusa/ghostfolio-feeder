"""Boerse Frankfurt module."""
from datetime import datetime
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def boerse_frankfurt(
        ticker: str, start_date: str | None = None, end_date: str | None = None
    ) -> list:
    """
    Fetches historical market data for a given ticker symbol from the Börse Frankfurt API.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get market data
    url = 'https://api.boerse-frankfurt.de/v1/tradingview/lightweight/history/single'
    query_params = {
        'resolution': 'D',
        'isKeepResolutionForLatestWeeksIfPossible': 'true',
        'from': '0000000000',
        'to': '9999999999',
        'isBidAskPrice': 'false',
        'symbols': ticker
    }
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.boerse-frankfurt.de',
        'Referer': 'https://www.boerse-frankfurt.de/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    response = requests.get(
        url,
        verify=False,
        params=query_params,
        headers=headers,
        timeout=10
    )
    market_data = response.json()[0]['quotes']['timeValuePairs']

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': float}
    market_data = [{
        "marketPrice": item["value"],
        "date": datetime.fromtimestamp(
            item["time"]
        ).strftime("%Y-%m-%d")
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(boerse_frankfurt("XETR:CH1199067674", start_date="2022-07-31"))


if __name__ == "__main__":
    main()
