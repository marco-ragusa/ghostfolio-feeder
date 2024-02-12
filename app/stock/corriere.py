from datetime import datetime
import requests
# Import utils
try:
    from stock import utils
except ImportError:
    import utils


def corriere(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    """
    Fetches historical market data for a given ticker symbol from Corriere API.

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
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': f'https://borsa.corriere.it/quotazione/?topicName={ticker}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    params = {
        'seriesType': 'Daily',
        # 'startTimepoint': '06^%^2F13^%^2F2023'
    }
    response = requests.get(
        f'https://borsa.corriere.it/api/TimeSeries/{ticker}',
        params=params,
        headers=headers,
        timeout=10,
    )
    market_data = response.json()['series']

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': int}
    market_data = [{
        "marketPrice": item["close"],
        "date": item["timestamp"].split('T')[0]
    } for item in market_data]

    # Fill missing dates
    end_date = end_date or datetime.today().strftime("%Y-%m-%d")
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


if __name__ == "__main__":
    utils.print_list(corriere("PEX0ALPFRA12.EUR", start_date="2000-01-01"))
