from .mvis import mvis
from .corriere import corriere
from .byblos import byblos
from .boerse_frankfurt import boerse_frankfurt
from .fondofonte import fondofonte
from .local import local


class Stock:
    """
    Represents a stock and provides methods to fetch data from different sources.

    Attributes:
        ticker (str): The ticker symbol of the stock.
        start_date (str): The start date for fetching data (optional).
        end_date (str): The end date for fetching data (optional).
    """

    def __init__(
            self, ticker: str, start_date: str | None = None, end_date: str | None = None
        ) -> None:
        if ticker is None:
            raise ValueError("To create the object you have to insert a ticker")
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date


    def mvis(self) -> list:
        """Fetches stock data from MVIS."""
        return mvis(self.ticker, self.start_date, self.end_date)

    def corriere(self) -> list:
        """Fetches stock data from Corriere."""
        return corriere(self.ticker, self.start_date, self.end_date)

    def byblos(self) -> list:
        """Fetches stock data from Byblos."""
        return byblos(self.ticker, self.start_date, self.end_date)

    def boerse_frankfurt(self) -> list:
        """Fetches stock data from Börse Frankfurt."""
        return boerse_frankfurt(self.ticker, self.start_date, self.end_date)

    def fondofonte(self) -> list:
        """Fetches stock data from Fondofonte."""
        return fondofonte(self.ticker, self.start_date, self.end_date)

    def local(self) -> list:
        """Fetches stock data from local source."""
        return local(self.ticker, self.start_date, self.end_date)


data_source_mapping = {
    "mvis": Stock.mvis,
    "corriere": Stock.corriere,
    "byblos": Stock.byblos,
    "boerse_frankfurt": Stock.boerse_frankfurt,
    "fondofonte": Stock.fondofonte,
    "local": Stock.local,
}
