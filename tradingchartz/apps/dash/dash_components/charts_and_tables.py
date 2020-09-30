# external standard
import pandas as pd
import datetime as dt

# external dash
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc

# internal import
import tradingchartz.apps.dash.helpers.helper_functions as hf


def generate_ohlc_graph(fig,
                        df) -> go.Figure:
    fig.add_trace(
        go.Ohlc(x=df.index.date,
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'],
                       name='OHLC')
    )
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(
                      xaxis=dict(
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=5,
                                       label="5d",
                                       step="day",
                                       stepmode="backward"),
                                  dict(count=1,
                                       label="1m",
                                       step="month",
                                       stepmode="backward"),
                                  dict(count=6,
                                       label="6m",
                                       step="month",
                                       stepmode="backward"),
                                  dict(count=1,
                                       label="YTD",
                                       step="year",
                                       stepmode="todate"),
                                  dict(count=1,
                                       label="1y",
                                       step="year",
                                       stepmode="backward"),
                                  dict(step="all")
                              ])
                          ),
                          range=[(min(df.index.date) - dt.timedelta(1)), (max(df.index.date) + dt.timedelta(1))],
                      ),
                      margin=dict(l=20, r=20, t=20, b=20))
    return fig


def add_signals_to_chart(fig: go.Figure,
                         signal_df: pd.DataFrame,
                         ohlc_df: pd.DataFrame) -> go.Figure:
    for pattern in signal_df.columns:
        up_signal, down_signal = hf.df_bifurcate_positive_and_negative_signals(signal_df[pattern])
        if not up_signal.empty:
            fig.add_trace(
                go.Scatter(
                    x=up_signal.index.date,
                    y=ohlc_df.loc[up_signal.index, 'High'],
                    mode='markers',
                    name=pattern,
                    marker_symbol='triangle-up',
                    marker=dict(
                        color='green',
                        size=10)
                )
            )
        if not down_signal.empty:
            fig.add_trace(
                go.Scatter(
                    x=down_signal.index.date,
                    y=ohlc_df.loc[down_signal.index, 'Low'],
                    mode='markers',
                    name=pattern,
                    marker_symbol='triangle-down',
                    marker=dict(
                        color='red',
                        size=10)
                )
            )
    return fig


def triple_barrier_setter_template():
    return [dbc.Row(
                [
                    dbc.Col(dbc.Label("Upper Barrier")),
                    dbc.Col(dbc.Input(id="tb-upper", placeholder="Profit Booking", type="float")),
                ], no_gutters=True),
            dbc.Row(
                [
                    dbc.Col(dbc.Label("Lower Barrier")),
                    dbc.Col(dbc.Input(id="tb-lower", placeholder="Stop Loss", type="float")),
                ], no_gutters=True),
            dbc.Row(
                [
                    dbc.Col(dbc.Label("Vertical Barrier")),
                    dbc.Col(dbc.Input(id="tb-vertical", placeholder="Time Horizon", type="float")),
                ], no_gutters=True),
            ]
