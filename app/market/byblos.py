"""Byblos module."""
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def byblos(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    """
    Fetches historical market data for a given ticker symbol from Byblos API.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get market data
    url = 'https://www.fondobyblos.it/grafici/tabella.php'
    query_params = {
        'c': ticker,
        'lang': 'it',
    }
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.fondobyblos.it',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    response = requests.get(
        url,
        verify=False,
        params=query_params,
        headers=headers,
        timeout=10,
    )
    market_data = response.json()

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': float}
    market_data = [{
        "marketPrice": float(item["valore"].replace(',','.')),
        "date": utils.convert_italian_date(item["data"])
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(byblos("211", "2000-01-01"))


if __name__ == "__main__":
    main()
