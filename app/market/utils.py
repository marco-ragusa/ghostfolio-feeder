"""Utils module."""
import random
from datetime import datetime, timedelta


def convert_italian_date(date_str) -> str:
    """
    Convert a date string in Italian format to 'yyyy-mm-dd' format.

    Args:
        date_str (str): The date string in Italian format, e.g., 'Gen 2021' or 'gennaio 2021'.

    Returns:
        str: The date string in 'yyyy-mm-dd' format, or None if the month is invalid.
    """
    # List of Italian month abbreviations
    italian_months = [
        'Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'
    ]

    # Split the date string into month and year
    parts = date_str.split(' ')
    # Check if the second element is a number (the year)
    if parts[1].isdigit():
        # Take only the first three letters and capitalize them
        month_str = parts[0][:3].capitalize()
        year_str = parts[1]
    # Otherwise, assume the first element is the year
    else:
        # Take only the first three letters and capitalize them
        month_str = parts[1][:3].capitalize()
        year_str = parts[0]

    # Check if the month is valid
    if month_str not in italian_months:
        return None  # Return None if the month is not valid

    # Get the month number
    month_number = italian_months.index(month_str) + 1

    # Build the date in 'yyyy-mm-dd' format
    return f'{year_str}-{month_number:02d}-01'


def fill_missing_dates(
        data_list, start_date: str | None = None, end_date: str | None = None
    ) -> list:
    """
    Fills a list of dictionaries with missing dates,
    inserting entries with the same marketPrice as the previous date.

    Args:
        data_list: A list of dictionaries with keys "marketPrice" and "date".

    Returns:
        A new list of dictionaries with all dates filled in.
    """
    # Add end_date if missing with current date
    end_date = end_date or datetime.today().strftime("%Y-%m-%d")

    # Sort data by date and remove duplicates
    data_list = sorted(data_list, key=lambda item: item["date"])
    data_list = remove_duplicates(data_list)
    filled_data_list = []

    # Add start and end dates if needed
    if start_date and start_date < data_list[0]["date"]:
        data_list.insert(0,
            {'date': start_date, "marketPrice": data_list[0]["marketPrice"]}
        )
    if end_date > data_list[-1]["date"]:
        data_list.append(
            {'date': end_date, "marketPrice": data_list[-1]["marketPrice"]}
        )

    last_date = None
    last_market_price = None

    for item in data_list:
        date = datetime.strptime(item["date"], "%Y-%m-%d").date()
        market_price = item["marketPrice"]

        # Fill in missing days between each data point (exclusive)
        if last_date:
            missing_dates = generate_missing_dates(last_date, date)
            filled_data_list.extend(
                {"date": str(date), "marketPrice": last_market_price} for date in missing_dates
            )

        # Add actual day
        filled_data_list.append({"date": str(date), "marketPrice": market_price})

        last_date = date
        last_market_price = market_price

    # Optionally filter by start and end dates
    if start_date:
        filled_data_list = [item for item in filled_data_list if item["date"] >= start_date]
    if end_date:
        filled_data_list = [item for item in filled_data_list if item["date"] <= end_date]

    return filled_data_list


def remove_duplicates(data_list) -> list:
    """
    Removes duplicate entries from a list of dictionaries based on the "date" key.

    Args:
        data_list: A list of dictionaries with a "date" key.

    Returns:
        A new list of dictionaries with the duplicate entries removed.
    """
    date_seen = set()
    unique_data_list = []

    for item in data_list:
        # Check if the date is already in the set
        if item["date"] not in date_seen:
            # Add the date to the set
            date_seen.add(item["date"])
            # Add the item to the new list
            unique_data_list.append(item)

    return unique_data_list


def generate_missing_dates(start_date, end_date):
    """
    Generates a generator of dates between start_date (exclusive) and end_date (exclusive).

    Args:
        start_date: The start date (exclusive).
        end_date: The end date (exclusive).

    Returns:
        A generator of dates between start_date and end_date.
    """

    current_date = start_date + timedelta(days=1)

    while current_date < end_date:
        yield current_date
        current_date += timedelta(days=1)


def print_list(market_price: list) -> None:
    """
    Prints a concise representation of a list of market prices.

    Args:
        marketPrice (list): A list of numerical market prices.
    """
    for price in market_price[:5] + ["..."] + market_price[-5:]:
        print(price)


def get_random_user_agent() -> str:
    """
    Returns a random user agent string from a static list.

    Returns:
        str: A random user agent string from the predefined list.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
            + " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)" \
            + " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
            + " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
            + " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0)" \
            + " Gecko/20100101 Firefox/121.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0)" \
            + " Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
            + "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Agency/99.8.2237.3",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0)" \
            + " Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 6.1)" \
            + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)" \
            + " Gecko/20100101 Firefox/117.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
            + "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4",
    ]

    return random.choice(user_agents)
