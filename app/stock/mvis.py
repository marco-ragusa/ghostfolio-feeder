import pandas as pd
import requests
# Import utils
try:
    from stock import utils
except ImportError:
    import utils


def mvis(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Api-Key': 'da2-5vmaeziahve2lorqvpvt65lspq',
        'x-amz-user-agent': 'aws-amplify/4.3.7 js',
        'Origin': 'https://www.marketvector.com',
        'Referer': 'https://www.marketvector.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    json_data = {
        'query': 'query GetMultipleChartData($ticker1: String, $timeRange1: String) {\n  ticker1: getMultipleChartData(IndexTicker: $ticker1, TimeRangeTypeName: $timeRange1) {\n    ticker\n    timestamp\n    y\n    indexType\n    timezone\n    timezoneOffset\n}\n}\n',
        'variables': {
            'ticker1': ticker,
            'timeRange1': 'Inception',
        },
    }
    response = requests.post(
        'https://wzszugyhvjh3bo4rqefrhsswdm.appsync-api.eu-central-1.amazonaws.com/graphql',
        headers=headers,
        json=json_data,
        timeout=10,
    )
    json_data = response.json()['data']['ticker1']

    # Convert JSON to DataFrame
    df = pd.json_normalize(json_data)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')

    # Set timestamp as index and rename to "date"
    df.set_index('timestamp', inplace=True)
    df.index.name = 'date'

    # Rename the "y" column to "marketPrice"
    df.rename(columns={'y': 'marketPrice'}, inplace=True)

    # Select only date index and marketPrice columns
    df = df[['marketPrice']]

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    utils.print_list(mvis("MVDA5", "2000-01-01"))
