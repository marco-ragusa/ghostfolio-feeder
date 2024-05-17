"""Cometa module."""
import re
from bs4 import BeautifulSoup, Comment
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def cometa_scraper(html: str) -> list:
    """
    Scrape market data from HTML content obtained from Cometa webpage.

    Args:
        html (str): The HTML content of the webpage.

    Returns:
        list: A list of dictionaries containing market data in the following format:
            [{'date': 'yyyy-mm-dd', 'marketPrice': str}]
    """
    # Create a dictionary to store the information
    market_data = []

    # Parsing HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find all comments in HTML
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    # Regex to extract date and price
    pattern = re.compile(r"new Date\((\d{4}),(\d{2}),(\d{2}),.*\),\s+([\d.]+)\s+\]")

    # Loop through the comments
    for comment in comments:
        match = pattern.search(comment)
        if match:
            year = match.group(1)
            month = int(match.group(2))+1 # +1 Because JS sucks
            day = match.group(3)
            price = match.group(4)
            date_str = f"{year}-{month}-{day}"
            market_data.append({'date': date_str, 'marketPrice': price})

    return market_data


def cometa(
        ticker: str, start_date: str | None = None, end_date: str | None = None
    ) -> list:
    """
    Fetches historical market data for a given ticker symbol from Cometa web page.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get web page
    url = f'https://www.cometafondo.it/quota/{ticker}/'
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Referer': url,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    # Make an HTTP request and get the content of the page
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
    )
    html = response.text

    # Extract market data from webpage
    market_data = cometa_scraper(html)

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': int}
    market_data = [{
        "marketPrice": float(item["marketPrice"]),
        "date": item["date"]
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(cometa("reddito", "2000-01-01"))


if __name__ == "__main__":
    main()
