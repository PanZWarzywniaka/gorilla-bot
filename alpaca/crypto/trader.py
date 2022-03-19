import yfinance as yf
import pandas as pd
import plotly.subplots as subplots
import plotly.graph_objects as go
import numpy as np
import pandas_ta as ta


class Trader:

    def __init__(self) -> None:
        self.dollars = 100
        self.asset = 0
        self.price_at_entry = None
        self.stop_loss_ratio = 0.990
        self.take_profit_ratio = 1.02
        self.rsi_threshold = 30
        self.ticker = "BTC-USD"
        self.period = "1mo"
        self.interval = "5m"
        self.rsi_signal = False

    def buy_all(self) -> bool:
        if self.dollars == 0:
            return False

        price_for_asset = self.candle_stick["Open"]
        self.asset = self.dollars/price_for_asset
        self.dollars = 0
        self.price_at_entry = price_for_asset

        print(f"Bought asset  " +
              f"Time: {self.candle_stick['Datetime']}")
        return True

    def sell_all(self) -> bool:
        if self.asset == 0:
            return False

        price_for_asset = self.candle_stick["Open"]

        print(f"Selling asset " +
              f"Time: {self.candle_stick['Datetime']}")
        print(
            f"\nProfit on trade: {(price_for_asset/self.price_at_entry-1)*100} % \n")

        self.dollars = self.asset*price_for_asset
        self.asset = 0
        self.price_at_entry = None
        self.rsi_signal = False

        return True

    def set_rsi_signal(self) -> bool:
        c = self.candle_stick
        if c['RSI_14'] < self.rsi_threshold:
            self.rsi_signal = True

    def buy_signal(self) -> bool:
        c = self.candle_stick
        ret = c['Crossover'] and c['Above'] and self.rsi_signal
        return ret

    def stop_loss_signal(self) -> bool:
        if self.price_at_entry is None:
            return False
        c = self.candle_stick
        return c['Open'] / self.price_at_entry <= self.stop_loss_ratio

    def take_profit_signal(self) -> bool:
        if self.price_at_entry is None:
            return False

        c = self.candle_stick
        return c['Open'] / self.price_at_entry >= self.take_profit_ratio

    def calculate_profit(self, df):
        df = df.reset_index()
        for _, candle_stick in df.iterrows():

            self.candle_stick = candle_stick

            self.set_rsi_signal()
            # buy
            if self.buy_signal():
                self.buy_all()

            # sell
            if self.stop_loss_signal() or self.take_profit_signal():
                self.sell_all()

        # end of time
        last_candle_stick = df.iloc[-1]
        self.sell_all()

    def download_data(self):
        df = yf.download(
            tickers=self.ticker,
            period=self.period,
            interval=self.interval,
            # start="2022-01-13",
            # end="2022-03-13"
        )
        df.rename(columns={'Datetime': 'index'}, inplace=True)
        print(df)
        return df

    def prepare_data(self, df):
        df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
        pd.set_option("display.max_columns", None)

        # pomarańczowe nad czarne
        df['Above'] = df['MACD_12_26_9'] >= df['MACDs_12_26_9']
        df['Crossover'] = df['Above'].diff()

        df.ta.rsi(close='Close', append=True)
        return df

    def make_charts(self, df):
        # Construct a 2 x 1 Plotly figure
        fig = subplots.make_subplots(rows=3, cols=1)
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
        # Rsi
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI_14'],
                line=dict(color='#52307c', width=2),
                name='RSI',
                # showlegend=False,
                legendgroup='rsi',
            ), row=3, col=1
        )
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=np.repeat(self.rsi_threshold, df.shape[0]),
                line=dict(color='#5230ff', width=2),
                name='RSI_threshold',
                # showlegend=False,
                legendgroup='rsi',
            ), row=3, col=1
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
