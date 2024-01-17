import requests
import pandas as pd
import locale
from bs4 import BeautifulSoup
# Import utils
try:
    import stock.utils as utils
except ImportError:
    import utils


def fondofonte(ticker: str, start_date: str | None = None, end_date: str | None = None) -> list:
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        f'Referer': 'https://www.fondofonte.it/gestione-finanziaria/i-valori-quota-dei-comparti/{ticker}/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    # Make an HTTP request and get the content of the page
    response = requests.get(
        f"https://www.fondofonte.it/gestione-finanziaria/i-valori-quota-dei-comparti/{ticker}/",
        headers=headers,
    )

    html = response.text

    # Create the BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with the class 'toggle-acf'
    toggle_elements = soup.find_all(class_='toggle-acf')

    # Create a dictionary to store the information
    fund_data = []

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
            fund_data.append({'date': f'{date} {year}', 'marketPrice': quote})

    # Create a DataFrame from the list of dictionaries
    df = pd.json_normalize(fund_data)

    # Convert data to datetime format
    locale.setlocale(locale.LC_ALL, 'it_IT')
    df['date'] = pd.to_datetime(df['date'], format='%B %Y')
    locale.setlocale(locale.LC_ALL, '')

    # Convert valore to float
    df['marketPrice'] = df['marketPrice'].str.replace(',', '.').astype(float)

    # Set timestamp as index and rename to "date"
    df.set_index('date', inplace=True)

    # Resample by day and select a date range
    df = utils.df_resample_range(df, start_date, end_date)

    # Convert to list with iso time format
    return utils.df_to_list(df)


if __name__ == "__main__":
    # utils.print_list(fondofonte("comparto-dinamico", "2008-05-01"))
    utils.print_list(fondofonte("comparto-dinamico", "2023-10-19"))
