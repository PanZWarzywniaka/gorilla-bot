import yfinance as yf
import pandas as pd
import plotly.subplots as subplots
import plotly.graph_objects as go
import numpy as np
import pandas_ta as ta


def make_charts(df):
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
    # Fast Signal (%k) uzywany pomarańczowy
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
    # Slow signal (%d) uzywany czarny
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


def calculate_profit(df):  # signals
    df = df.reset_index()
    dollars = 100
    coin = 0
    bought = False
    for index, r in df.iterrows():
        if r['Crossover'] and r['Above'] and not bought:  # signal to buy
            price_for_coin = r['Open']
            coin = dollars/price_for_coin
            dollars = 0
            bought = True
            break

        if r['Crossover'] and not r['Above'] and bought:  # signal to sell
            price_for_coin = r['Open']
            dollars = coin*price_for_coin
            coin = 0
            bought = False
            break

    # end of time
    if bought:
        last_row = df.iloc[-1]
        price_for_coin = last_row['Close']
        dollars = coin*price_for_coin
        coin = 0
        bought = False

    return dollars


def main():
    df = yf.download(
        tickers="BTC-USD",
        period="1d",
        interval="5m",
        # start="2022-01-13",
        # end="2022-03-13"
    )

    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    pd.set_option("display.max_columns", None)

    # pomarańczowe nad czarne
    df['Above'] = df['MACD_12_26_9'] >= df['MACDs_12_26_9']
    # df2 = df['Diff']
    # df2['Index'] = df.index
    # print(df2)
    # print(df2.shape)
    df['Crossover'] = df['Above'].diff()
    df_signals = df[df['Crossover'] != 0]

    print(df_signals)
    print(df_signals.shape)

    profit = calculate_profit(df_signals)
    print(profit)
    make_charts(df)


if __name__ == '__main__':
    main()
