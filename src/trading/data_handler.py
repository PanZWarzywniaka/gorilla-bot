from models.candlestick import Candlestick


class DataHandler():
    def __init__(self,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m",
                 ) -> None:

        self.data = Candlestick.download_yahoo_candlestics(
            ticker, period, interval)

        # db test
        Candlestick.save(self.data)
        self.data = Candlestick.load()

        self.data = Candlestick.process_candlestics(self.data)
