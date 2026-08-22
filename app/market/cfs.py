"""Colonial First State (CFS) market data source."""

from datetime import date, datetime
from functools import cache

from http_client import request

from . import utils

CFS_DOWNLOAD_URL = (
    "https://www.colonialfirststate.com.au/Price_Performance/Download.aspx"
)
CFS_FUNDS_URL = (
    "https://secure.colonialfirststate.com.au/fp/pricenperformance/products/funds"
)
CFS_REFERER = (
    "https://www.cfs.com.au/personal/resources/"
    "funds-and-performance/funds-and-performance-search.html"
)
CFS_FUND_URLS = (
    f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=IF&expand=false&"
    "productId=91&productId=70&productId=90",
    f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=SF&expand=false&"
    "productId=11&productId=65",
    f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=RF&expand=false&productId=51",
    f"{CFS_FUNDS_URL}?companyCode=001&mainGroup=WF&expand=false&"
    "productId=120&productId=91&productId=73",
)


def _headers(accept: str) -> dict:
    return {
        "User-Agent": utils.BROWSER_USER_AGENT,
        "Accept": accept,
        "Accept-Language": "en-AU,en;q=0.9",
        "Referer": CFS_REFERER,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }


@cache
def download_funds() -> dict:
    """Download the APIR-to-product mapping."""
    funds = {}
    for url in CFS_FUND_URLS:
        response = request("GET", url, headers=_headers("application/json, */*"))
        for fund in response.json()["funds"]:
            funds[fund["apir"]] = {
                "mainGroup": fund["mainGroup"],
                "productID": fund["ivstGrup"],
                "fundID": fund["cfsCodeVal"],
            }

    return funds


def cfs(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> list:
    """Fetch historical prices from CFS."""
    start_date = start_date or "2000-01-01"
    end_date = end_date or date.today().isoformat()

    from_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    to_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")

    product_info = download_funds().get(ticker)

    if not product_info:
        raise ValueError(f"No product information found for APIR code: {ticker}")

    market_data = []
    params = {
        "hidDLTab": "History",
        "hidDLMainGroup": product_info["mainGroup"],
        "hidDLProductIDs": product_info["productID"],
        "hidDLFundIDs": product_info["fundID"],
        "hidDLFromDate": from_date,
        "hidDLToDate": to_date,
    }

    with request(
        "GET",
        CFS_DOWNLOAD_URL,
        params=params,
        headers=_headers("text/csv,application/octet-stream,*/*"),
        stream=True,
    ) as response:
        for line in response.iter_lines():
            if not line:
                continue
            values = line.decode("utf-8").split(",")
            market_data.append(
                {
                    "date": datetime.strptime(values[0], "%d/%m/%Y").date().isoformat(),
                    "marketPrice": float(values[3]),
                }
            )

    return utils.fill_missing_dates(market_data, start_date, end_date)
