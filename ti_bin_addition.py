import pandas as pd

tb_detail_data = pd.read_csv(r'/mnt/E/py_WorkingDirectory/Technical Analysis/TradingChartz/TB_Analysis_detailed_with_2_10.csv')

tb_detail_data.set_index(['Date', 'ticker'], inplace=True)

ti_list = ['RSI', 'RSI20', 'MFI', 'CCI', 'WILLR']
for ti_name in ti_list:
    ti_signal_bin_detail = pd.read_csv(rf'/home/jasmeet/Dropbox/BackTestResults/TA_Lib_TI_rolling_BBG_data/{ti_name}_all_ticker.csv')
    ti_signal_bin_detail.set_index(['Date', 'Ticker'], inplace=True)
    tb_detail_data[f'{ti_name} Bin Labels'] = ti_signal_bin_detail.loc[ti_signal_bin_detail.index, 'Bin Labels']


tb_detail_data.to_csv('TB_details_with_TI_bins_on_signal_with_2_10.csv')

