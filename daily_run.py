import talib
import pandas as pd


import datetime as dt
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData

nsepy_obj = NSEPyData()
index_constituents = nsepy_obj.get_index_constituents('NIFTY 500')
final_df = pd.DataFrame()
signal_final_list = []
for ticker in index_constituents.Symbol:
    candle_names = talib.get_function_groups()['Pattern Recognition']
    df_price_data = nsepy_obj.historical_stock_close_price(ticker, dt.date(2020, 11, 1), dt.date(2020, 11, 27))
    value_check = df_price_data.Close.isnull().values.any()
    if value_check or df_price_data.empty:
        continue
    print(ticker)
    for candle_pattern in candle_names:
        signal_sr = getattr(talib, candle_pattern)(df_price_data[f"Open"],
                                                   df_price_data[f"High"],
                                                   df_price_data[f"Low"],
                                                   df_price_data[f"Close"])
        index = ticker + candle_pattern
        final_df.loc[index, 'pattern'] = candle_pattern
        final_df.loc[index, 'ticker'] = ticker
        final_df.loc[index, 'Signal'] = signal_sr.values[-1]
        final_df.loc[index, 'Open'] = df_price_data["Open"].iloc[-1]
        final_df.loc[index, 'High'] = df_price_data[f"High"].iloc[-1]
        final_df.loc[index, 'Low'] = df_price_data[f"Low"].iloc[-1]
        final_df.loc[index, 'Close'] = df_price_data[f"Close"].iloc[-1]

final_df_non_zero = final_df[final_df['Signal'] != 0]
final_df_non_zero.reset_index(drop=True).to_csv('daily_run27112020o.csv')