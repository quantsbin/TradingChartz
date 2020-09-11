# external standards
import datetime as dt
import pandas as pd


def string_to_date(date_: str):
    return dt.datetime.strptime(date_, '%Y-%m-%d')


def df_from_jason(json_data: str) -> pd.DataFrame:
    return pd.read_json(json_data, orient='index')
