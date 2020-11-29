from pandas_datareader import get_data_yahoo as data
import datetime as dt

test = data('TEJASNET.NS', '2010-01-01', '2020-11-24')

import talib
import pandas as pd

import datetime as dt
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData

nsepy_obj = NSEPyData()
index_constituents = nsepy_obj.get_index_constituents('NIFTY 500')
# final_df = pd.DataFrame()
# signal_final_list = []
# for ticker in index_constituents.Symbol[]:
#     candle_names = talib.get_function_groups()['Pattern Recognition']
#     df_price_data = data(ticker+'.NS', '2020-11-1', '2020-11-27')
#     df_price_data = df_price_data.round(2)
#     value_check = df_price_data.Close.isnull().values.any()
#     if value_check or df_price_data.empty:
#         continue
#     print(ticker)
#     for candle_pattern in candle_names:
#         signal_sr = getattr(talib, candle_pattern)(df_price_data[f"Open"],
#                                                    df_price_data[f"High"],
#                                                    df_price_data[f"Low"],
#                                                    df_price_data[f"Close"])
#         index = ticker + candle_pattern
#         final_df.loc[index, 'pattern'] = candle_pattern
#         final_df.loc[index, 'ticker'] = ticker
#         final_df.loc[index, 'date'] = signal_sr.index[-1]
#         final_df.loc[index, 'Signal'] = signal_sr.values[-1]
#         final_df.loc[index, 'Open'] = df_price_data["Open"].iloc[-1]
#         final_df.loc[index, 'High'] = df_price_data[f"High"].iloc[-1]
#         final_df.loc[index, 'Low'] = df_price_data[f"Low"].iloc[-1]
#         final_df.loc[index, 'Close'] = df_price_data[f"Close"].iloc[-1]
#
# final_df_non_zero = final_df[final_df['Signal'] != 0]
# final_df_non_zero.reset_index(drop=True).to_csv('daily_run27112020.csv')

x = 0
list_data = []
increment = 5
t0 = dt.datetime.now()
while x <= len(index_constituents.Symbol.values):
    if x+increment > len(index_constituents.Symbol.values):
        _data = data((index_constituents.Symbol.values + '.NS')[x:], '2020-11-1', '2020-11-27')
    else:
        _data =data((index_constituents.Symbol.values + '.NS')[x:x+increment], '2020-11-1', '2020-11-27')
    list_data.append(_data)
    x = x + increment
    print(x)
    ti = dt.datetime.now()
    diffi = (ti-t0)
    print(diffi.total_seconds())
df = pd.concat(list_data, axis=1)
t1 = dt.datetime.now()
diff = t1-t0
print(diff.total_seconds())