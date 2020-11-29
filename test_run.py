import pandas as pd
from tradingchartz.src.data_sourcing.csv_data import BBGcsvData
import talib

csv_data_retriver = BBGcsvData(file_path='OHLCv_6_Nov_2020_10y.csv')
ticker_list = csv_data_retriver.available_tickers
ticker_list.sort()
# ohlcv = csv_data_retriver.get_OHLCv_data(ticker='AXSB')
# ohlcv.to_csv("AXSB.csv")

macd_output_list = []
name = 'CCI'
bins = [-1000, -100, 0, 100, 1000]
labels = [1, 2, 3, 4]
for ticker in ticker_list:
    ohlcv = csv_data_retriver.get_OHLCv_data(ticker=ticker)
    if ohlcv.empty:
        continue
    ohlcv.dropna(how='any', inplace=True)
    open = ohlcv['Open']
    high = ohlcv['High']
    low = ohlcv['Low']
    close = ohlcv['Close']
    volume = ohlcv['Vol']

    upperband = talib.CCI(high, low, close, timeperiod=23)
    upperband.rename(name, inplace=True)

    macd = pd.concat([upperband], axis=1)
    macd['Ticker'] = ticker
    macd_output_list.append(macd)

macd_output = pd.concat(macd_output_list, axis=0)
#
macd_output = macd_output[['Ticker', name]]
macd_output['Bins'] = pd.cut(macd_output[name], bins=bins)
macd_output['Bin Labels'] = pd.cut(macd_output[name], bins=bins, labels=labels)
macd_output.to_csv(f"{name}_all_ticker.csv")




# end

