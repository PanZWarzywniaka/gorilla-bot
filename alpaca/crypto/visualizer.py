import plotly.subplots as subplots
import plotly.graph_objects as go
import numpy as np


class Visualizer:

    def __init__(self, df, rsi_threshold) -> None:

        # Construct a 2 x 1 Plotly figure
        fig = subplots.make_subplots(rows=3, cols=1)
        # price Line

        # signals
        for row in range(3):  # 00FF00 green #FF0000 red
            for index, signal_cs in df.loc[df['Action'] != 0].iterrows():
                fig.add_vline(x=index,
                              line_color="green", row=row+1, col=1)
            # fig.append_trace(
            #     go.Scatter(
            #         x=df.index,
            #         y=df[f'RSI_{self.rsi_length}'],
            #         line=dict(color='#52307c', width=2),
            #         name='RSI',
            #         # showlegend=False,
            #         legendgroup='rsi',
            #     ), row=row, col=1
            # )

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
                y=df['RSI'],
                line=dict(color='#52307c', width=2),
                name='RSI',
                # showlegend=False,
                legendgroup='rsi',
            ), row=3, col=1
        )
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=np.repeat(rsi_threshold, df.shape[0]),
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
