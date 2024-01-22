import locale
import pandas as pd
import requests
# Import utils
try:
    from stock import utils
except ImportError:
    import utils


def byblos(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
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

    json_data = response.json()

    # Convert JSON to DataFrame
    df = pd.json_normalize(json_data)

    # Convert data to datetime format
    locale.setlocale(locale.LC_ALL, 'it_IT')
    df['timestamp'] = pd.to_datetime(df['data'], format='%B %Y')
    locale.setlocale(locale.LC_ALL, '')

    # Convert valore to float
    df['valore'] = df['valore'].str.replace(',', '.').astype(float)

    # Set timestamp as index and rename to "date"
    df.set_index('timestamp', inplace=True)
    df.index.name = 'date'

    # Rename the "close" column to "marketPrice"
    df.rename(columns={'valore': 'marketPrice'}, inplace=True)

    # Select only Date index and marketPrice columns
    df = df[['marketPrice']]

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    utils.print_list(marketPrice = byblos("211", "2000-01-01"))
