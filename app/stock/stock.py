from .yahoo_finance import yahoo_finance
from .mvis import mvis
from .corriere import corriere
from .byblos import byblos
from .boerse_frankfurt import boerse_frankfurt
from .fondofonte import fondofonte


class Stock:
    def __init__(self, ticker: str, start_date: str | None = None, end_date: str | None = None) -> None:
        if ticker is None:
            raise ValueError("To create the object you have to insert a ticker")
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
    
    def yahoo_finance(self) -> list:
        return yahoo_finance(self.ticker, self.start_date, self.end_date)
    
    def mvis(self) -> list:
        return mvis(self.ticker, self.start_date, self.end_date)
        
    def corriere(self) -> list:
        return corriere(self.ticker, self.start_date, self.end_date)
    
    def byblos(self) -> list:
        return byblos(self.ticker, self.start_date, self.end_date)

    def boerse_frankfurt(self) -> list:
        return boerse_frankfurt(self.ticker, self.start_date, self.end_date)

    def fondofonte(self) -> list:
        return fondofonte(self.ticker, self.start_date, self.end_date)


data_source_mapping = {
    "yahoo_finance": Stock.yahoo_finance,
    "mvis": Stock.mvis,
    "corriere": Stock.corriere,
    "byblos": Stock.byblos,
    "boerse_frankfurt": Stock.boerse_frankfurt,
    "fondofonte": Stock.fondofonte,
}