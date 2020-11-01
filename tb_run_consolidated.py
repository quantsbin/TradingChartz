from nsepy import get_history
from datetime import date, timedelta
import pandas as pd

# from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData
from tradingchartz.src.data_sourcing.csv_data import BBGcsvData
from tradingchartz.src.backtesting.triple_barrier import TripleBarrier, TripleBarrierCalculator, TripleBarrierSetter

# end_day = date.today()
# start_day = end_day - timedelta(1250)
#
# csv_data_retriver = BBGcsvData(file_path='OHLCv.csv')
# print(csv_data_retriver.available_tickers)
# print(csv_data_retriver.get_OHLCv_data(ticker='EIM'))
#
# def nse_stock():
#         df = NSEPyData.historical_stock_close_price(symbol='HDFCAMC',
#                                                     start_date=start_day,
#                                                     end_date=end_day)
#         return df
# # print()
#
# # print(NSEPyData.get_symbol_list('index')['Codes'].to_list())
#
# # print(NSEPyData.get_index_constituents('NIFTY BANK').head().T)
#
# df = nse_stock()
#
# df.to_csv("stock_data.csv")

import talib
print(help(talib.CDLDOJI))
#
# output = talib.CDLDOJI(df.Open, df.High, df.Low, df.Close)
# # print(df)
# # print(output.head())
# output = output[output.values > 0]
# # output['entry_price'] = df.shift(-1).loc[output.index, 'Open']
# print(output.head())
#
# # test = output.to_frame(name='signals')
# # test['entry_price'] = df.shift(-1).loc[output.index, 'Open']
# # print(df.loc[date(2017, 1, 16), 'Open'])
# # print(test)
#
#
# triple_barrier = TripleBarrierSetter(.1, .05, 20)
# triple_test = TripleBarrierCalculator(triple_barrier,
#                                       df,
#                                       output)
#
# print(triple_test.df_signal_with_barrier.T)
# triple_test.df_triple_barrier_details.to_csv("tb_test.csv")
# print(triple_test.get_triple_barrier_summary(triple_test.df_triple_barrier_details))
#
#
csv_data_retriver = BBGcsvData(file_path='OHLCv_8_Oct_2020.csv')
# print(csv_data_retriver.available_tickers)
# print(csv_data_retriver.get_OHLCv_data(ticker='EIM'))

candle_names = talib.get_function_groups()['Pattern Recognition']
print(candle_names)
print(csv_data_retriver)
print(csv_data_retriver.raw_data)
signal_df = pd.DataFrame(index=csv_data_retriver.raw_data.index)
print(signal_df)

signal_summary_df = pd.DataFrame(index=csv_data_retriver.available_tickers)
print(signal_summary_df)

triple_barrier = TripleBarrierSetter(6, 3, 65, 'ATR')
buffer_value= 0
print(triple_barrier)
# triple_test = TripleBarrierCalculator(triple_barrier,
#                                       df,
#                                       output)
tb_candle_consolidation_list = []
tb_summary_df = pd.DataFrame(index=csv_data_retriver.available_tickers)
for candle in candle_names:
    signal_df = pd.DataFrame(index=csv_data_retriver.raw_data.index)
    for i, ticker in enumerate(csv_data_retriver.available_tickers):
        # print(ticker)
        df = csv_data_retriver.get_OHLCv_data(ticker)
        temp_df_atr = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=10).fillna(method='bfill')
        df['ATR'] = temp_df_atr

        # df['preceding_low_adj'] = df['Close'] - (1-buffer_value)*df['Low_0_1']
        signal_sr = getattr(talib, candle)(df[f"Open"],
                                           df[f"High"],
                                           df[f"Low"],
                                           df[f"Close"])
        signal_df[ticker] = signal_sr
        signal_summary_df.loc[ticker, f'Total_{candle}'] =  len(signal_df[~(signal_df[ticker].values == 0)])
        signal_summary_df.loc[ticker, f'Positive_{candle}'] = len(signal_df[(signal_df[ticker].values > 0)])
        signal_summary_df.loc[ticker, f'Negative_{candle}'] = len(signal_df[(signal_df[ticker].values < 0)])
        signal_sr = signal_sr[(signal_sr.values > 0)]
        if len(signal_sr) > 0:
            triple_test = TripleBarrierCalculator(triple_barrier,
                                                  df,
                                                  signal_sr[(signal_sr.values > 0)])
            triple_barrier_details = triple_test.df_triple_barrier_details
            triple_barrier_details['ticker'] = ticker
            triple_barrier_details['candle_pattern'] = candle
            # ticker_temp = ticker.replace(r"/", "")
            tb_candle_consolidation_list.append(triple_barrier_details)
            # triple_barrier_details.to_csv(rf"TB_Files_updated_preceding_low/{candle}_{ticker_temp}_2to1_65.csv")
            if "barrier_type" not in triple_barrier_details.columns:
                continue
            _temp_tb_summary = triple_test.get_triple_barrier_summary(triple_barrier_details)
            if "lower" in _temp_tb_summary.index:
                tb_summary_df.loc[ticker, f'{candle}_lower'] = _temp_tb_summary.loc['lower', 'barrier_count']
            else:
                tb_summary_df.loc[ticker, f'{candle}_lower'] = 0
            if "upper" in _temp_tb_summary.index:
                tb_summary_df.loc[ticker, f'{candle}_upper'] = _temp_tb_summary.loc['upper', 'barrier_count']
            else:
                tb_summary_df.loc[ticker, f'{candle}_upper'] = 0
            if "vertical" in _temp_tb_summary.index:
                tb_summary_df.loc[ticker, f'{candle}_vertical'] = _temp_tb_summary.loc['vertical', 'barrier_count']
            else:
                tb_summary_df.loc[ticker, f'{candle}_vertical'] = 0
        print(f'progress for {candle} - {(i/502)*100}%')
    print(f"completed {candle}")
if tb_candle_consolidation_list:
    candle_tb_details = pd.concat(tb_candle_consolidation_list)
        # candle_tb_details.to_csv(rf"TB_Files/{candle}.csv")
    # signal_df.to_csv(f"Signal_Files_updated/{candle}_output.csv")


candle_tb_details.to_csv('TB_Analysis_detailed_with_ATR3.csv')

tb_summary_df.to_csv(r"tb_summary_with_ATR3.csv")
# signal_summary_df.to_csv(r"signal_summary.csv")



