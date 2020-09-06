import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import datetime as dt

from tradingchartz.src.data_sourcing.nsepy_data import NSEPyData

data = NSEPyData.historical_stock_close_price('sbin', dt.date(2020, 1, 1), dt.date.today())
fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])],
                layout=dict(xaxis={'type': 'category'},
                            height=800))
fig.update_layout(xaxis_rangeslider_visible=False)
print(data.columns)
print(data.index)

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''Dash Framework: A web application framework for Python.'''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)