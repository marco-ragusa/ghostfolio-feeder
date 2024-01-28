import pandas as pd
import requests
# Import utils
try:
    from stock import utils
except ImportError:
    import utils


def boerse_frankfurt(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    
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
        f'https://api.boerse-frankfurt.de/v1/tradingview/lightweight/history/single?resolution=D&isKeepResolutionForLatestWeeksIfPossible=false&from=0000000000&to=9999999999&isBidAskPrice=false&symbols={ticker}',
        headers=headers,
        timeout=10,
    )

    json_data = response.json()[0]['quotes']['timeValuePairs']

    # Convert JSON to DataFrame
    df = pd.json_normalize(json_data)

    # Parse time to date and convert it to DateTime
    df['time'] = pd.to_datetime(df['time'], utc=True, unit='s').dt.date
    df['time'] = pd.to_datetime(df['time'])

    # Set time as index and rename to "date"
    df.set_index('time', inplace=True)
    df.index.name = 'date'

    # Rename the "value" column to "marketPrice"
    df.rename(columns={'value': 'marketPrice'}, inplace=True)
   
    # Select only Date index and marketPrice columns
    df = df[['marketPrice']]

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    utils.print_list(boerse_frankfurt("XETR:CH1199067674", "2022-07-31"))
