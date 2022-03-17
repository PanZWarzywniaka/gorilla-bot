import yfinance as yf
import pandas as pd
import plotly.subplots as subplots
import plotly.graph_objects as go
import numpy as np
import pandas_ta as ta


def main():
    df = yf.download(
        tickers="BTC-USD",
        period="2d",
        interval="1m",
        # start="2022-01-13",
        # end="2022-03-13"
    )
    print(df.shape)
    # k = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()

    # macd = k - d
    # macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # macd_h = macd - macd_s
    # df['macd'] = df.index.map(macd)
    # df['macd_h'] = df.index.map(macd_h)
    # df['macd_s'] = df.index.map(macd_s)

    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    pd.set_option("display.max_columns", None)
    print(df)
    # Construct a 2 x 1 Plotly figure
    fig = subplots.make_subplots(rows=2, cols=1)
    # price Line
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['Open'],
            line=dict(color='#ff9900', width=1),
            name='Open',
            # showlegend=False,
            legendgroup='1',
        ), row=1, col=1
    )
    # Candlestick chart for pricing
    fig.append_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
        ), row=1, col=1
    )
    # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['MACD_12_26_9'],
            line=dict(color='#ff9900', width=2),
            name='MACD',
            # showlegend=False,
            legendgroup='2',
        ), row=2, col=1
    )
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['MACDs_12_26_9'],
            line=dict(color='#000000', width=2),
            # showlegend=False,
            legendgroup='2',
            name='signal'
        ), row=2, col=1
    )
    # Colorize the histogram values
    colors = np.where(df['MACDh_12_26_9'] < 0, '#000', '#ff9900')
    # Plot the histogram
    fig.append_trace(
        go.Bar(
            x=df.index,
            y=df['MACDh_12_26_9'],
            name='histogram',
            marker_color=colors,
        ), row=2, col=1
    )
    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )
    # Update options and show plot
    fig.update_layout(layout)
    fig.show()


if __name__ == '__main__':
    main()
