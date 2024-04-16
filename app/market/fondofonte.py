from bs4 import BeautifulSoup
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def fondofonte(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    """
    Fetches historical market data for a given ticker symbol from Fondo Fon.Te web page.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': int}
    """

    # Get web page
    base_url = f'https://www.fondofonte.it/gestione-finanziaria/i-valori-quota-dei-comparti/{ticker}/'
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Referer': base_url,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }
    # Make an HTTP request and get the content of the page
    response = requests.get(
        base_url,
        headers=headers,
        timeout=10,
    )
    html = response.text

    # Create the BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with the class 'toggle-acf'
    toggle_elements = soup.find_all(class_='toggle-acf')

    # Create a dictionary to store the information
    market_data = []

    # Iterate through all toggle elements
    for toggle in toggle_elements:
        # Extract the year from the toggle title string
        year = toggle.a.text

        # Find the content of the next toggle (containing the quote information)
        toggle_content = toggle.find_next(class_='toggle-content-acf')

        # Extract all rows of quote information
        quote_rows = toggle_content.find_all(class_='toggle_element_row')

        # Iterate through all quote information rows
        for quote_row in quote_rows:
            # Extract the date and quote from the row
            date = quote_row.find('span', {'class': None}).text.strip()
            if date in 'Periodo':
                continue
            quote = quote_row.find_all('span', {'class': None})[1].text.strip()

            # Add the information to the list
            market_data.append({'date': f'{date} {year}', 'marketPrice': quote})

    # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': int}
    market_data = [{
        "marketPrice": float(item["marketPrice"].replace(',','.')),
        "date": utils.convert_italian_date(item["date"])
    } for item in market_data]

    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


if __name__ == "__main__":
    utils.print_list(fondofonte("comparto-dinamico", start_date="2023-10-19"))
