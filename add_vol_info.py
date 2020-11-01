import pandas as pd
import numpy as np
import os

base_df = pd.read_csv(r'/mnt/E/py_WorkingDirectory/Technical Analysis/TradingChartz/tb_summary.csv', index_col=0)


df = pd.DataFrame(index=base_df.index, columns=base_df.columns)

DIRECTORY = r'/mnt/E/py_WorkingDirectory/Technical Analysis/TradingChartz/TB_Files'

for column_name in df.columns:
    file_name = column_name.split('_')[0] + '.csv'
    temp_df = pd.read_csv(os.path.join(DIRECTORY, file_name))
    for index_value in df.index:
        file_name = column_name.split('_')[0]+'.csv'
        if pd.isnull(base_df.loc[index_value, column_name]):
            df.loc[index_value, column_name] = np.nan
        elif base_df.loc[index_value, column_name] == 0:
            df.loc[index_value, column_name] = np.nan
        else:

            df.loc[index_value, column_name] = temp_df[(temp_df['barrier_type']==column_name.split('_')[1]) &
                                                       (temp_df['ticker']==index_value)]['holding_period_td'].mean()

df.to_csv('holding_period.csv')





