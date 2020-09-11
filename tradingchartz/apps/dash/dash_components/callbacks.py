# external standard
import datetime as dt
from typing import Any

# dash imports
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

# internal imports
import tradingchartz.apps.dash.helpers.helper_functions as hf
import tradingchartz.apps.dash.dash_components.charts_and_tables as cts
from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData


def register_main_page_callbacks(app: Any) -> Any:

    @app.callback(
        Output('selected-stock-dropdown', 'options'),
        [
            Input('selected-universe-dropdown', 'value'),
        ]
    )
    def set_stock_selection_list(universe_symbol: str):
        index_constituents = NSEPyData.get_index_constituents(universe_symbol)
        stock_options = [{'label': row['Company Name'],
                          'value': row['Symbol']} for _, row in index_constituents.iterrows()]
        return stock_options

    @app.callback(
        Output('stock-ohlcv-data', 'data'),
        [
            Input('selected-stock-dropdown', 'value'),
            Input('stock-data-date-range', 'start_date'),
            Input('stock-data-date-range', 'end_date')
        ]
    )
    def fetch_price_data(stock_symbol: str,
                         start_date: str,
                         end_date: str) -> str:
        if (start_date is None) or (end_date is None) or (stock_symbol is None):
            raise PreventUpdate
        start_date = hf.string_to_date(start_date)
        end_date = hf.string_to_date(end_date)
        df = NSEPyData.historical_stock_close_price(stock_symbol, start_date, end_date)
        return df.to_json(orient='index', date_format='iso')

    @app.callback(
        Output('stock-ohlc-chart', 'figure'),
        [
            Input('stock-ohlcv-data', 'data')
        ]
    )
    def generate_ohlc_graph(stock_ohlcv_data: str) -> go.Figure():
        stock_ohlcv_df = hf.df_from_jason(stock_ohlcv_data)
        return cts.generate_ohlc_graph(stock_ohlcv_df)