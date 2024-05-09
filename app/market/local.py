"""Local module."""
import csv
import json
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def local(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    """
    Retrieve market data for a given ticker from a JSON or CSV file.

    Args:
        ticker (str): The ticker symbol for the market data.
        start_date (str, optional): The start date in "YYYY-MM-DD" format. Defaults to None.
        end_date (str, optional): The end date in "YYYY-MM-DD" format. Defaults to None.

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}

    Raises:
        ValueError: If the file format is not supported. Only JSON or CSV files are supported.
    """
    # Define the file path
    file_path = ticker

    # Check if file ends with ".json" or ".csv".
    if not file_path.lower().endswith((".json", ".csv")):
        raise ValueError("File format not supported. Only use JSON or CSV.")

    market_data = []

    # JSON or CSV parsing
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.lower().endswith(".json"):
            market_data = json.load(file)
        elif file_path.lower().endswith(".csv"):
            csv_reader = csv.DictReader(file)
            market_data = list(csv_reader)

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(local("app/data/local/example.json", start_date="2019-01-01"))


if __name__ == "__main__":
    main()
