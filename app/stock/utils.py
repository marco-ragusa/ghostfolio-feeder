import json
import random
from datetime import date
import pandas as pd


def df_resample_range(df: pd.DataFrame, start_date: str | None = None, end_date: str | None = None) -> pd.DataFrame:
    # Sort df by index
    df = df.sort_index()

    # Remove duplicates from index
    df = df[~df.index.duplicated(keep='last')]

    # Fill missing dates in index
    df = df.resample('D').ffill()

    # Add firt date (start_date) if not present
    if (start_date is not None and
        start_date not in df.index):
        first_marketPrice = df['marketPrice'].iloc[0]
        first_row = pd.DataFrame({'marketPrice': [first_marketPrice]}, index=[pd.Timestamp(start_date)])
        df = pd.concat([first_row, df])

    # Add last day (today) if not present
    today = date.today()
    if today not in df.index:
        last_marketPrice = df['marketPrice'].iloc[-1]
        last_row = pd.DataFrame({'marketPrice': [last_marketPrice]}, index=[pd.Timestamp(today)])
        df = pd.concat([df, last_row])

    # Select only defined Date range
    df = df.loc[start_date:end_date]

    # Remove duplicates from index
    df = df[~df.index.duplicated(keep='last')]

    # Fill new missing dates in index
    return df.resample('D').ffill()


def df_to_list(df: pd.DataFrame) -> list:
    # Index to column
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})

    # Convert to list
    return json.loads(
        df.to_json(
            orient="records",
            date_format='iso', 
            date_unit = 's'
        )
    )


def print_list(marketPrice: list) -> list:
    for price in marketPrice[:5] + ["..."] + marketPrice[-5:]:
        print(price)


def get_random_user_agent() -> str:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Agency/99.8.2237.3",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4",
    ]

    return random.choice(user_agents)
