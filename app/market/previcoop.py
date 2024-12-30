"""Previdenza Cooperativa module."""
from bs4 import BeautifulSoup
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def previcoop_scraper(html: str) -> list:
    """
    Scrape market data from HTML content obtained from Previdenza Cooperativa webpage.

    Args:
        html (str): The HTML content of the webpage.

    Returns:
        list: A list of dictionaries containing market data in the following format:
            [{'date': 'yyyy-mm-dd', 'marketPrice': str}]
    """
    # Create a dictionary to store the information
    market_data = []

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table body
    table_body = soup.find('table', {'id': 'table_4'}).find('tbody')

    # Extract data from the table
    for row in table_body.find_all('tr'):
        cells = row.find_all('td')
        # Check if the row contains exactly 3 cells (date, market price, patrimonio)
        if len(cells) == 3:
            # Extracting date and market price from the cells
            date = cells[0].text.strip()
            market_price = cells[1].text.strip()
            # Append the extracted data to the list
            market_data.append({'date': date, 'marketPrice': market_price})

    return market_data


def previcoop(
        ticker: str, start_date: str | None = None, end_date: str | None = None
    ) -> list:
    """
    Fetches historical market data for a given ticker symbol from Previdenza Cooperativa web page.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get web page
    url = f'https://www.previdenzacooperativa.it/{ticker}/'
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
    market_data = previcoop_scraper(html)

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': int}
    market_data = [{
        "marketPrice": float(item["marketPrice"].replace(',','.')),
        "date": f"{item["date"][-4:]}-{item["date"][3:5]}-{item["date"][:2]}"
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(previcoop("comparto-dinamico", "2019-01-01"))


if __name__ == "__main__":
    main()
