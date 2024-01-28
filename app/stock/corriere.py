import pandas as pd
import requests
# Import utils
try:
    from stock import utils
except ImportError:
    import utils


def corriere(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
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

    json_data = response.json()['series']

    # Convert JSON to DataFrame
    df = pd.json_normalize(json_data)

    # Parse timestamp to date and convert it to DateTime
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True).dt.date
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set timestamp as index and rename to "date"
    df.set_index('timestamp', inplace=True)
    df.index.name = 'date'

    # Rename the "close" column to "marketPrice"
    df.rename(columns={'close': 'marketPrice'}, inplace=True)

    # Select only Date index and marketPrice columns
    df = df[['marketPrice']]

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    utils.print_list(corriere("PEX0ALPFRA12.EUR", "2000-01-01"))
