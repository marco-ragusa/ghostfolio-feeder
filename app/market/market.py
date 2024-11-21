"""Market module."""
from .mvis import mvis
from .corriere import corriere
from .byblos import byblos
from .boerse_frankfurt import boerse_frankfurt
from .fondofonte import fondofonte
from .mediafond import mediafond
from .previcoop import previcoop
from .cometa import cometa
from .cfs import cfs
from .local import local


class Market:
    """
    Represents the market and provides methods to fetch data from different sources.

    Attributes:
        ticker (str): The ticker symbol of the asset.
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
        """Fetches market data from MVIS."""
        return mvis(self.ticker, self.start_date, self.end_date)

    def corriere(self) -> list:
        """Fetches market data from Corriere."""
        return corriere(self.ticker, self.start_date, self.end_date)

    def byblos(self) -> list:
        """Fetches market data from Byblos."""
        return byblos(self.ticker, self.start_date, self.end_date)

    def boerse_frankfurt(self) -> list:
        """Fetches market data from Börse Frankfurt."""
        return boerse_frankfurt(self.ticker, self.start_date, self.end_date)

    def fondofonte(self) -> list:
        """Fetches market data from Fondofonte."""
        return fondofonte(self.ticker, self.start_date, self.end_date)

    def mediafond(self) -> list:
        """Fetches market data from MEDIAFOND."""
        return mediafond(self.ticker, self.start_date, self.end_date)

    def previcoop(self) -> list:
        """Fetches market data from Previdenza Cooperativa."""
        return previcoop(self.ticker, self.start_date, self.end_date)

    def cometa(self) -> list:
        """Fetches market data from Investing."""
        return cometa(self.ticker, self.start_date, self.end_date)

    def cfs(self) -> list:
        """Fetches market data from Colonial First State."""
        return cfs(self.ticker, self.start_date, self.end_date)

    def local(self) -> list:
        """Fetches market data from local source."""
        return local(self.ticker, self.start_date, self.end_date)


data_source_mapping = {
    "mvis": Market.mvis,
    "corriere": Market.corriere,
    "byblos": Market.byblos,
    "boerse_frankfurt": Market.boerse_frankfurt,
    "fondofonte": Market.fondofonte,
    "mediafond": Market.mediafond,
    "previcoop": Market.previcoop,
    "cometa": Market.cometa,
    "cfs": Market.cfs,
    "local": Market.local,
}
