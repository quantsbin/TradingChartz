import pandas as pd
import numpy as np
import datetime as dt
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData
from tradingchartz.src.backtesting.triple_barrier import TripleBarrier, TripleBarrierCalculator, TripleBarrierSetter

tb_data = pd.read_csv(r'/home/jasmeet/Dropbox/BackTestResults/TB_BackTest/TB_Candle_BackTest_t_1_t_low_2_close_entry/TB_details_with_TI_bins_on_signal.csv')
signal_dates = tb_data['Date'].unique()

index_signal_sr = pd.Series(np.ones(len(signal_dates))*100, index=signal_dates)
index_signal_sr.index = pd.to_datetime(index_signal_sr.index).date
index_signal_sr.sort_index(inplace=True)

nsepy_obj = NSEPyData()

print(nsepy_obj.get_symbol_list('index'))

index_constituents = nsepy_obj.get_index_constituents('NIFTY 500')

price_50 = nsepy_obj.historical_index_close_levels('NIFTY 50', dt.date(2010, 1, 1))
price_100 = nsepy_obj.historical_index_close_levels('NIFTY 100', dt.date(2010, 1, 1))
price_500 = nsepy_obj.historical_index_close_levels('NIFTY 500', dt.date(2010, 1, 1))

price_50.to_csv('NIFTY50_OHLCV.csv')
price_50.rename(columns = {'Volume': 'Vol'}, inplace=True)
price_100.to_csv('NIFTY100_OHLCV.csv')
price_100.rename(columns = {'Volume': 'Vol'}, inplace=True)
price_500.to_csv('NIFTY500_OHLCV.csv')
price_500.rename(columns = {'Volume': 'Vol'}, inplace=True)


triple_barrier = TripleBarrierSetter(2, 65, 'preceding_low_adj')
buffer_value = 0
# print(ticker)
df = price_500
df['Low_1'] = df['Low'].shift(1)
df['Low_0_1'] = df[['Low_1', 'Low']].min(axis=1)
df['preceding_low_adj'] = df['Close'] - (1-buffer_value)*df['Low_0_1']
signal_sr = index_signal_sr

triple_test = TripleBarrierCalculator(triple_barrier,
                                  df,
                                  signal_sr[(signal_sr.values > 0)])
triple_barrier_details = triple_test.df_triple_barrier_details
triple_barrier_details.to_csv('index_tb_summary_nifty500.csv')
