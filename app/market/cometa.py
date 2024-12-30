"""Cometa module."""
from datetime import datetime
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
            [{'date': 'mm/yyyy', 'marketPrice': str}]
    """
    # Parsing HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table with id="table_2" and get the data-wpdatatable_id attribute
    table_2 = soup.find('table', id="table_2")
    if not table_2 or not table_2.has_attr('data-wpdatatable_id'):
        raise Exception("Table with id='table_2' or data-wpdatatable_id attribute not found.")

    wpdatatable_id = table_2['data-wpdatatable_id']

    # Regular expression to match the id of <tr>
    id_pattern = re.compile(f"^table_{wpdatatable_id}_row_\d+$")

    # Find all <tr> elements matching the criteria
    rows = soup.find_all('tr', id=id_pattern, attrs={'data-row-index': True})

    # Extract the first two <td> elements of each <tr>
    market_data = []
    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 2:
            market_data.append({'date': tds[0].get_text(strip=True), 'marketPrice': tds[1].get_text(strip=True)})

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
        verify=False,
        headers=headers,
        timeout=10,
    )
    html = response.text

    # Extract market data from webpage
    market_data = cometa_scraper(html)

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': int}
    market_data = [{
        "marketPrice": float(item["marketPrice"].replace(',','.')),
        "date": datetime.strptime(
            item["date"], "%m/%Y"
        ).strftime("%Y-%m-%d")
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(cometa("crescita", "2000-01-01"))


if __name__ == "__main__":
    main()
