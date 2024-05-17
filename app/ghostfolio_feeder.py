"""Ghostfolio Feeder module."""
from datetime import datetime, timedelta
from ghostfolio import Ghostfolio
from market import Market, data_source_mapping


def subtract_days_from_date(input_date: str, days_to_subtract: int = 0) -> str:
    """Subtract a specified number of days from the given date.

    Args:
        input_date (str): The input date in 'YYYY-MM-DD' format.
        days_to_subtract (int, optional): The number of days to subtract. Defaults to 0.

    Returns:
        str: The new date as a string in 'YYYY-MM-DD' format.
    """
    # Convert the date string to a datetime object
    input_date = datetime.strptime(input_date, '%Y-%m-%d')

    # Calculate the new date by subtracting the desired days
    result_date = input_date - timedelta(days=days_to_subtract)

    # Return the new date as a string in the format 'YYYY-MM-DD'.
    return result_date.strftime('%Y-%m-%d')


def get_market_data(data_source: dict) -> dict:
    """Retrieve market data for the specified data source.

    Args:
        data_source (dict): A dictionary containing data source details

    Returns:
        dict: A dictionary containing the market data.
    """
    # Create an instance of the Market class with the specified ticker and start date
    market_instance = Market(ticker=data_source['ticker'], start_date=data_source['start_date'])

    # Call the appropriate method from the data_source_mapping using the market_instance
    market_data = data_source_mapping[data_source['name']](market_instance)

    return {
        # 'marketData': [{"marketPrice":666.00,"date":"2024-01-01T00:00:00.000Z"}],
        'marketData': market_data,
    }


def ghostfolio_feeder(
        host: str, access_token: str, symbol: str, profile_data: dict, data_source: dict
    ) -> None:
    """Feed data into Ghostfolio by creating profiles and populating market data.

    Args:
        host (str): The Ghostfolio host URL.
        access_token (str): The access token for authentication.
        symbol (str): The symbol for which to manage data.
        profile_data (dict): The profile data to set.
        data_source (dict): The data source details for fetching market data.
    """
    ghostfolio = Ghostfolio(host, access_token, symbol)

    # Create data profile if not exist
    if not ghostfolio.profile_data_is_exist():
        ghostfolio.create_profile_data()
        ghostfolio.set_profile_data(profile_data)

    # Populate data from the last 90 days
    if ghostfolio.market_data_is_exist():
        last_date = ghostfolio.get_last_market_data()['date'].split('T')[0]
        data_source['start_date'] = subtract_days_from_date(last_date, 90)
        ghostfolio.populate_market_data(get_market_data(data_source))
    else:
        ghostfolio.populate_market_data(get_market_data(data_source))
