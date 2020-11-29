import datetime as dt
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData


nsepy_obj = NSEPyData()

print(nsepy_obj.get_symbol_list('index'))

# index_constituents = nsepy_obj.get_index_constituents('NIFTY 500')
# print(index_constituents.Symbol)

# index_constituents.to_csv('nifty_500_constituents.csv')

price = nsepy_obj.historical_stock_close_price('NIFTY 50', dt.date(2020, 10, 5))

price.to_csv('test_price.csv')