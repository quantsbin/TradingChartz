import pandas as pd
from tradingchartz.src.data_sourcing.csv_data import BBGcsvData
import talib

csv_data_retriver = BBGcsvData(file_path='OHLCv_8_Oct_2020.csv')
ticker_list = csv_data_retriver.available_tickers
ticker_list.sort()
ohlcv = csv_data_retriver.get_OHLCv_data(ticker='AXSB')
ohlcv.to_csv("AXSB.csv")

macd_output_list = []
name = 'BBANDS'
for ticker in ['HDFCAMC']:
    ohlcv = csv_data_retriver.get_OHLCv_data(ticker=ticker)
    ohlcv = ohlcv.dropna()
    open = ohlcv['Open']
    high = ohlcv['High']
    low = ohlcv['Low']
    close = ohlcv['Close']
    volume = ohlcv['Vol']

    upperband= talib.ATR(high, low, close, timeperiod=10)
    upperband.rename('upperband', inplace=True)

    macd = pd.concat([upperband], axis=1)
    macd['Ticker'] = ticker
    macd_output_list.append(macd)

macd_output = pd.concat(macd_output_list, axis=0)
#
# macd_output = macd_output[['Ticker', 'upperband', 'middleband', 'lowerband']]
# macd_output.to_csv(f"{name}_all_ticker.csv")