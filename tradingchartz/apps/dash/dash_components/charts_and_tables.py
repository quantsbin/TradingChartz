import plotly.graph_objects as go


def generate_ohlc_graph(df):
    fig = go.Figure(data=[go.Candlestick(x=df.index.date,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(xaxis_type='category',
                      margin=dict(l=20, r=20, t=20, b=20))
    return fig