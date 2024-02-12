from datetime import datetime
import requests
# Import utils
try:
    from stock import utils
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
            {'date': 'yyyy-mm-dd', 'marketPrice': int}
    """

    # Get market data
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.fondobyblos.it',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    params = {
        'c': ticker,
        'lang': 'it',
    }
    response = requests.get(
        'https://www.fondobyblos.it/grafici/tabella.php',
        params=params,
        headers=headers,
        timeout=10,
    )
    market_data = response.json()

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': int}
    market_data = [{
        "marketPrice": float(item["valore"].replace(',','.')),
        "date": utils.convert_italian_date(item["data"])
    } for item in market_data]

    # Fill missing dates
    end_date = end_date or datetime.today().strftime("%Y-%m-%d")
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


if __name__ == "__main__":
    utils.print_list(marketPrice = byblos("211", "2000-01-01"))
