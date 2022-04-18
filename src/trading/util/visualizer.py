from datetime import datetime
import plotly.subplots as subplots
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from models.trade import Trade
from models.candlestick import Candlestick


class Visualizer:

    def __init__(self, start: datetime = None, end: datetime = None):
        self.df = Candlestick.get_processed_candlesticks().loc[start:end]
        self.trades = Trade.load(start, end)

        self.rsi_threshold = 30
        self.__set_layout()
        # initialize 3x1 figure
        self.fig = subplots.make_subplots(
            rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.005)
        self.__draw()

    def __draw(self):
        # 1st chart
        self.__prices_chart(1, 1)
        # 2nd chart
        self.__macd_chart(2, 1)
        # 3rd chart
        self.__rsi_chart(3, 1)

        # Update options and show plot
        self.fig.update_layout(self.layout)
        pio.renderers.default = 'browser'
        pio.show(self.fig)

    def __candlesticks(self, row, col):
        # Candlestick chart for pricing
        self.fig.append_trace(
            go.Candlestick(
                x=self.df.index,
                open=self.df['open'],
                high=self.df['high'],
                low=self.df['low'],
                close=self.df['close'],
                increasing_line_color='#ff9900',
                decreasing_line_color='black',
                showlegend=False
            ), row=row, col=col
        )

    def __scatter_line(self, row, col, colour: str, column_name: str):
        self.fig.append_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df[column_name],
                line=dict(color=colour, width=2),
                name=column_name,
                # showlegend=False,
                legendgroup='2',
            ), row=row, col=col
        )

    def __histogram(self, row, col, colour1: str, colour2: str, column_name: str):
        # Colorize the histogram values
        colors = np.where(self.df[column_name] < 0, colour1, colour2)
        # Plot the histogram
        self.fig.append_trace(
            go.Bar(
                x=self.df.index,
                y=self.df[column_name],
                name='histogram',
                marker_color=colors,
            ), row=row, col=col
        )

    def __show_trades(self, row, col):
        trade_list = list(self.trades.itertuples())
        for t in trade_list:
            # buy
            self.fig.add_vline(t.buy_datetime,
                               line_color="green", row=row, col=col)
            # sell
            self.fig.add_vline(t.sell_datetime,
                               line_color="red", row=row, col=col)

    def __prices_chart(self, row, col):  # 1st
        self.__scatter_line(row, col, '#ff9900', "open")
        self.__candlesticks(row, col)
        self.__show_trades(row, col)

    def __macd_chart(self, row, col):  # 2nd
        # Fast Signal ( % k)  # orange
        self.__scatter_line(row, col, '#ff9900', 'macd_fast')

        # Slow signal (%d) #black
        self.__scatter_line(row, col, '#000000', 'macd_slow')

        # Plot the histogram
        self.__histogram(row, col, '#000', '#ff9900', 'macd_hist')

    def __rsi_chart(self, row, col):

        # RSI
        self.__scatter_line(row, col, '#52307c', "rsi")
        # RSI_threshold
        self.fig.add_hline(y=self.rsi_threshold,
                           line_color='#5230ff', row=3, col=1)

    def __set_layout(self):
        # Make it pretty
        self.layout = go.Layout(
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
