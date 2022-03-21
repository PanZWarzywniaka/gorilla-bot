import plotly.subplots as subplots
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np


class Visualizer:

    def __price_line(self, row, col):
        # Open price Line
        self.fig.append_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df['Open'],
                line=dict(color='#ff9900', width=1),
                name='Open',
                # showlegend=False,
                legendgroup='1',
            ), row=row, col=col
        )

    def __candlesticks(self, row, col):
        # Candlestick chart for pricing
        self.fig.append_trace(
            go.Candlestick(
                x=self.df.index,
                open=self.df['Open'],
                high=self.df['High'],
                low=self.df['Low'],
                close=self.df['Close'],
                increasing_line_color='#ff9900',
                decreasing_line_color='black',
                showlegend=False
            ), row=row, col=col
        )

    def __prices_chart(self, row, col):
        self.__price_line(row, col)
        self.__candlesticks(row, col)

    def __init__(self, df, rsi_threshold) -> None:
        self.df = df
        # Construct a 2 x 1 Plotly self.figure
        self.fig = subplots.make_subplots(
            rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.005)

        # 1st chart
        self.__prices_chart(1, 1)
        # signals

        for index, signal_cs in self.df.loc[self.df['Action'] == 2].iterrows():
            self.fig.add_vline(x=index,
                               line_color="green", row=1, col=1)
        for index, signal_cs in self.df.loc[self.df['Action'] == 3].iterrows():
            self.fig.add_vline(x=index,
                               line_color="red", row=1, col=1)

        # 1st Chart

        # 2nd Chart
        # Fast Signal (%k) #orange
        self.fig.append_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df['MACD_12_26_9'],
                line=dict(color='#ff9900', width=2),
                name='MACD',
                # showlegend=False,
                legendgroup='2',
            ), row=2, col=1
        )

        # Slow signal (%d) #black
        self.fig.append_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df['MACDs_12_26_9'],
                line=dict(color='#000000', width=2),
                # showlegend=False,
                legendgroup='2',
                name='signal'
            ), row=2, col=1
        )

        # Colorize the histogram values
        colors = np.where(self.df['MACDh_12_26_9'] < 0, '#000', '#ff9900')
        # Plot the histogram
        self.fig.append_trace(
            go.Bar(
                x=self.df.index,
                y=self.df['MACDh_12_26_9'],
                name='histogram',
                marker_color=colors,
            ), row=2, col=1
        )

        # 3rd chart
        # RSI LINE
        self.fig.append_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df['RSI'],
                line=dict(color='#52307c', width=2),
                name='RSI',
                # showlegend=False,
                legendgroup='rsi',
            ), row=3, col=1
        )

        # RSI treshold
        self.fig.append_trace(
            go.Scatter(
                x=self.df.index,
                y=np.repeat(rsi_threshold, self.df.shape[0]),
                line=dict(color='#5230ff', width=2),
                name='RSI_threshold',
                # showlegend=False,
                legendgroup='rsi',
            ), row=3, col=1
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
        self.fig.update_layout(layout)
        pio.renderers.default = 'browser'
        pio.show(self.fig)
