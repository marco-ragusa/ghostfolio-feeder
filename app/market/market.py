"""Available market data sources."""

from .boerse_frankfurt import boerse_frankfurt
from .byblos import byblos
from .cfs import cfs
from .cometa import cometa
from .corriere import corriere
from .fondofonte import fondofonte
from .local import local
from .mediafond import mediafond
from .previcoop import previcoop


data_source_mapping = {
    "boerse_frankfurt": boerse_frankfurt,
    "byblos": byblos,
    "cfs": cfs,
    "cometa": cometa,
    "corriere": corriere,
    "fondofonte": fondofonte,
    "local": local,
    "mediafond": mediafond,
    "previcoop": previcoop,
}
