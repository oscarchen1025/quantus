import pandas as pd
import plotly.graph_objects as go


def plot_klines(ohlcv,title=None,end_date=None,n_bars=180):

    s = ohlcv.copy().loc[:end_date or pd.to_datetime('now')].tail(n_bars)

    fig = go.Figure(data=[go.Candlestick(x=s.index,open=s['open'],high=s['high'],low=s['low'],close=s['close'],increasing_line_color='#ba4545',decreasing_line_color='#27847c')])

    fig.update_xaxes(rangebreaks=[dict(values=s.reindex(pd.date_range(s.index[0],s.index[-1])).pipe(lambda s:s[s['close'].isna()]).index)])
    fig.update_layout(width=1300,height=500,title=title,template='plotly_dark',plot_bgcolor='#1a1b20',paper_bgcolor='#1a1b20')
    fig.show()