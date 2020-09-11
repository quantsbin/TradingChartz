# external standard
import datetime as dt

# internal packages
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData

DEFAULT_UNIVERSE = "NIFTY 50"
DEFAULT_START_DATE = dt.date.today() - dt.timedelta(365)
DEFAULT_END_DATE = dt.date.today()

UNIVERSE_LIST = NSEPyData.get_symbol_list('index')['Codes'].to_list()
