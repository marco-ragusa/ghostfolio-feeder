"""MarketVector module."""
from datetime import datetime
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def mvis(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    """
    Fetches historical market data for a given ticker symbol from MarketVector API.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get market data
    url = 'https://wzszugyhvjh3bo4rqefrhsswdm.appsync-api.eu-central-1.amazonaws.com/graphql'
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Api-Key': 'da2-gnchylboffdibdgdd4lkpiy2de',
        'x-amz-user-agent': 'aws-amplify/4.7.14 js',
        'Origin': 'https://www.marketvector.com',
        'Referer': 'https://www.marketvector.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    json = {
        'query': \
        """
        query GetMultipleChartData($ticker1: String, $timeRange1: String) {
            ticker1: getMultipleChartData(IndexTicker: $ticker1, TimeRangeTypeName: $timeRange1) {
                timestamp
                y
            }
        }
        """,
        'variables': {
            'ticker1': ticker,
            'timeRange1': 'Inception',
        },
    }
    response = requests.post(
        url,
        verify=False,
        headers=headers,
        json=json,
        timeout=10,
    )
    market_data = response.json()['data']['ticker1']

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': float}
    market_data = [{
        "marketPrice": item["y"],
        "date": datetime.fromtimestamp(
            int(item["timestamp"])
        ).strftime("%Y-%m-%d")
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(mvis("MVDA5", start_date="2000-01-01"))


if __name__ == "__main__":
    main()
