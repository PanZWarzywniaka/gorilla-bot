from models.candlestick import Candlestick
from models.trade import Trade
from trader import Trader


class HistoricalTrader(Trader):
    def __init__(self,
                 clear_db=True,
                 update_db=True,
                 dollars=100,
                 starting_asset=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m") -> None:
        super().__init__(clear_db,
                         update_db,
                         dollars,
                         starting_asset,
                         take_profit_ratio,
                         stop_loss_ratio,
                         rsi_threshold,
                         ticker,
                         period,
                         interval)

        Trade.clear_table()
        self.data = Candlestick.get_processed_candlesticks()
        self.run_historical_simulation()
        self.print_stats()

    def run_historical_simulation(self):

        df = self.data.reset_index()
        for _, candlestick in df.iterrows():
            self.take_action(candlestick)

        # end of time
        self.candlestick = df.iloc[-1]  # last candle stick
        self.sell_all()
        print(f"MONEY: {self.dollars} $$$")
