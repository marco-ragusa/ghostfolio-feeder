"""Colonial First State (CFS) module."""

from datetime import datetime
from functools import cache
import requests
import sqlite3

CFS_DOWNLOAD_URL = (
    "https://www.colonialfirststate.com.au/Price_Performance/Download.aspx"
)
CFS_FUNDS_URL = (
    "https://secure.colonialfirststate.com.au/fp/pricenperformance/products/funds"
)

funds_db = sqlite3.connect("file::memory:?cache=shared")

# Import utils
try:
    from market import utils
except ImportError:
    import utils


# If we wanted to make this "even more cachey", we could save the results to a local sqlite3 file on disk.
# This would mean that we wouldn't need to download the fund details every time ghostfolio-feeder started.
# But we would need to delete the sqlite database file in order to force a re-download.
@cache
def download_funds():
    print("CFS: Downloading fund info")
    cur = funds_db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS fund(apir VARCHAR PRIMARY KEY, main_group VARCHAR, product_id INTEGER, fund_id INTEGER)"
    )

    # From reverse engineering what the Fund and Performance page is doing
    # See https://www.cfs.com.au/personal/resources/funds-and-performance/funds-and-performance-search.html
    # FirstChoice Wholesale Investments - IF - 91
    # FirstChoice Investments - IF - 70
    # Managed Investment Funds - IF - 90
    # FirstChoice Wholesale Personal Super - SF - 11
    # FirstChoice Employer Super - SF - 65
    # FirstChoice Wholesale Pension - RF - 51
    # Institutional and Master trusts - WF - 120, 91, 73
    for url in [
        f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=IF&expand=false&productId=91&productId=70&productId=90",
        f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=SF&expand=false&productId=11&productId=65",
        f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=RF&expand=false&productId=51",
        f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=WF&expand=false&productId=120&productId=91&productId=73",
    ]:
        r = requests.get(url)
        for fund in r.json()["funds"]:
            if not fund["termDeposit"]:
                cur.execute(
                    "INSERT INTO fund(apir, main_group, product_id, fund_id) VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING",
                    (
                        fund["apir"],
                        fund["mainGroup"],
                        fund["ivstGrup"],
                        fund["cfsCodeVal"],
                    ),
                )
    cur.close()
    funds_db.commit()


@cache
def product_info_from_apir(apir_code: str) -> dict:
    download_funds()
    print(f"CFS: Looking up product info for {apir_code}")
    cur = funds_db.cursor()
    res = cur.execute(f"SELECT main_group, product_id, fund_id FROM fund WHERE apir = '{apir_code}'")
    data = res.fetchone()
    cur.close()
    return {"mainGroup": data[0], "productID": data[1], "fundID": data[2]}


def cfs(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """
    Fetches historical market data for a given ticker symbol from the Colonial First State performance tool.

    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).

    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    if start_date is None:
        start_date = "2000-01-01"
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    from_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    to_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    product_info = product_info_from_apir(ticker)

    market_data = []

    params = {
        "hidDLTab": "History",
        "hidDLMainGroup": product_info["mainGroup"],
        "hidDLProductIDs": product_info["productID"],
        "hidDLFundIDs": product_info["fundID"],
        "hidDLFromDate": from_date,
        "hidDLToDate": to_date,
    }

    # curl 'https://www.colonialfirststate.com.au/Price_Performance/Download.aspx?hidDLProductIDs=11&hidDLFundIDs=41&hidDLMainGroup=SF&hidDLFromDate=01/01/2000&hidDLToDate=11/11/2024&hidDLTab=History'
    s = requests.Session()

    with s.get(CFS_DOWNLOAD_URL, params=params, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                # We use naive CSV parsing, since the returned data is very simple
                # The format of the file is `Date in %d/%M/%Y,Entry Price,<Unknown>,Exit Price`
                # The Exit Price is the price used in the value calculations ith the CFS dashboard/app
                csv_data = line.decode("utf-8").split(",")

                # Format market data in this way {'date': 'yyyy-mm-dd', 'marketPrice': float}
                data = {
                    "date": datetime.strptime(csv_data[0], "%d/%m/%Y").strftime(
                        "%Y-%m-%d"
                    ),
                    "marketPrice": float(csv_data[3]),
                }
                market_data.append(data)

    # Fill missing dates
    market_data = utils.fill_missing_dates(
        market_data, start_date=start_date, end_date=end_date
    )

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(cfs("FSF0581AU", start_date="2004-07-15"))
    utils.print_list(cfs("FSF0618AU", start_date="2004-07-15"))
    utils.print_list(cfs("FSF0618AU", start_date="2004-07-15"))


if __name__ == "__main__":
    main()
