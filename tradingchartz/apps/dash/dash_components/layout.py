# external standard
import datetime as dt

# external dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

# internal package
import tradingchartz.apps.dash.helpers.defaults_and_enums as de
from tradingchartz.apps.dash.dash_components.store import main_store


layout_top_bars = dbc.Col(
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Universe", className="mr-2"),
                            dcc.Dropdown(id='selected-universe-dropdown',
                                         options=[{'label': symbol, 'value': symbol} for symbol in de.UNIVERSE_LIST],
                                         value=de.DEFAULT_UNIVERSE,
                                         placeholder="Select index",
                                         clearable=False),
                        ],
                        className="mr-3",
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Stock", className="mr-2"),
                            dcc.Dropdown(id='selected-stock-dropdown',
                                         value="State bank of India",
                                         placeholder="Select Stock"),
                        ],
                        className="mr-3"
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Date-Range", className="mr-2"),
                            dcc.DatePickerRange(
                                id='stock-data-date-range',
                                start_date_placeholder_text='Start Date',
                                start_date=de.DEFAULT_START_DATE,
                                end_date=de.DEFAULT_END_DATE,
                                max_date_allowed=dt.date.today(),
                                day_size=30
                            )
                        ],
                        className="mt-4"
                    )
                ),
            ]),
        ]),
        className="w-100"), width=11)

layout_main_side_body = dbc.Card(
    [
        dbc.CardHeader("Indicators"),
        dbc.CardBody(
            [
                dbc.Label("Select Candle Pattern"),
                dcc.Dropdown(id='selected-candle-pattern-dropdown',
                             options=[{'label': symbol, 'value': symbol} for symbol in de.CANDLE_PATTERNS],
                             # value,
                             placeholder="Select Pattern",
                             clearable=False,
                             multi=True,
                             style=dict(width='100%'))
            ]
            )
    ], className="w-100")

layout_main_charting_body = dbc.Card(
    [dbc.CardHeader("Stock Name and other information"),
     dbc.CardBody([dcc.Graph(id='stock-ohlc-chart')])
     ], className="w-100")


# dbc.Row(),  # TODO: Additional graphs.

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(html.H1("Trading-Chartz", className="text-center")
                    , className="mb-1 mt-1")
        ]),
        dbc.Row(layout_top_bars, justify="center"),
        dbc.Row(
            [
                dbc.Col(layout_main_side_body, width=2),
                dbc.Col(layout_main_charting_body, width=9)
            ], justify="center"),
        dbc.Row()  # TODO: Work on back-testing result body template.
    ] + main_store,
    className="dash-bootstrap"
)
