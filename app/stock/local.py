import pandas as pd
# Import utils
try:
    from stock import utils
except ImportError:
    import utils


def local(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    # Define the file path
    file_path = f"app/data/local/{ticker}"

    # Check if file ends with ".json" or ".csv".
    if not file_path.lower().endswith((".json", ".csv")):
        raise ValueError("Formato del file non supportato. Utilizzare solo JSON o CSV.")

    # JSON or CSV to DataFrame
    if file_path.lower().endswith(".json"):
        df = pd.read_json(file_path)
    elif file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path)

    # Select only the desired columns
    df = df[["date", "marketPrice"]]

    # Convert data to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Set date as index
    df.set_index('date', inplace=True)

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    utils.print_list(local("example.csv"))
