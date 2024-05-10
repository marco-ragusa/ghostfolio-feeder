"""Investing module."""
from datetime import datetime
import time
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def fetch_data_with_retry(url, params=None, headers=None, key=None, retry_count=5) -> any:
    """
    Fetches data from a given URL with retry mechanism.

    Args:
        url (str): The URL to fetch data from.
        params (dict, optional): The parameters to be sent with the request. Defaults to None.
        headers (dict, optional): The HTTP headers to be sent with the request. Defaults to None.
        key (str, optional): The key to access the desired data in the response. Defaults to None.
        retry_count (int, optional): The number of retry attempts in case of failure. Defaults to 5.

    Returns:
        any: The fetched data.

    Raises:
        ValueError: If unable to get response after all retry attempts.
    """
    data = ""

    while retry_count > 0:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10,
        )
        # Check if retry is needed
        if "Just a moment..." in response.text:
            time.sleep(1)
            retry_count -= 1 # Decrement the retry count
        else:
            data = response.json()[key]
            break

    if retry_count == 0 and data == "":
        raise ValueError(f"Error: Unable to get response after {retry_count} attempts.")

    return data


def get_symbol_id(ticker: dict) -> int:
    """
    Retrieves the unique identifier (ID) of a financial symbol.

    Args:
        ticker (dict): A dictionary containing information about the ticker symbol.

    Raises:
        ValueError: If the symbol does not exist or if it is too generic.

    Returns:
        int: The unique identifier (ID) of the symbol.
    """
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'domain-id': ticker["domain"],
        'Origin': f'https://{ticker["domain"]}.investing.com',
        'Referer': f'https://{ticker["domain"]}.investing.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    params = {
        'q': ticker["symbol"],
    }

    quotes = fetch_data_with_retry(
        url='https://api.investing.com/api/search/v2/search',
        params=params,
        headers=headers,
        key="quotes",
        retry_count=ticker["retry"]
    )

    filtered_quotes = [
        item for item in quotes if item['exchange'].lower() == ticker['exchange'].lower()
    ]

    filtered_quotes = [
        item for item in filtered_quotes if item['symbol'].lower() == ticker['symbol'].lower()
    ]

    # Check if the filter was successful
    if len(filtered_quotes) < 1:
        raise ValueError("The symbol does not exist, make sure you use a correct one.")
    if len(filtered_quotes) > 1:
        raise ValueError("The symbol is too generic, be sure to use a more specific one.")

    return filtered_quotes[0]["id"]


def investing(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    """
    Fetches historical market data for a given ticker symbol from Investing API.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    symbol_id = get_symbol_id(ticker)

    # Get market data
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'domain-id': ticker["domain"],
        'Origin': f'https://{ticker["domain"]}.investing.com',
        'Referer': f'https://{ticker["domain"]}.investing.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    params = {
        'period': 'MAX',
        'interval': 'P1D',
        'pointscount': '160',
    }

    market_data = fetch_data_with_retry(
        url=f'https://api.investing.com/api/financialdata/{symbol_id}/historical/chart/',
        params=params,
        headers=headers,
        key="data",
        retry_count=ticker["retry"]
    )

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': float}
    market_data = [{
        "marketPrice": item[4],
        "date": datetime.fromtimestamp(
            item[0] / 1000
        ).strftime("%Y-%m-%d")
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(investing(
        {
            "domain": "www",
            "symbol": "spy",
            "exchange": "nyse",
            "retry": 5
        },
        "2000-01-01"
    ))


if __name__ == "__main__":
    main()
