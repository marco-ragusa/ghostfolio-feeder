import yfinance as yf
import pandas as pd
# Import utils
try:
    import stock.utils as utils
except ImportError:
    import utils


def yahoo_finance(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    # Get stock historical data
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)

    # Convert index from Timestamp to Date and remove timezone
    df.index = pd.to_datetime(df.index).tz_localize(None)

    # Rename index to "date"
    df.index.name = 'date'

    # Rename the "close" column to "marketPrice"
    df.rename(columns={'Close': 'marketPrice'}, inplace=True)

    # Make a DF with index and marketPrice column
    df = df[['marketPrice']]

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    utils.print_list(yahoo_finance("VWCE.DE","2019-01-01"))
