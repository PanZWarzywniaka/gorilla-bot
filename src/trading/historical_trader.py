from trader import Trader
from models.trade import Trade


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
        Trade.clear_table(Trade)
        self.run_historical_simulation()

    def run_historical_simulation(self):

        df = self.data.reset_index()
        for index, c in df.iterrows():

            self.index = index
            self.candlestick = c

            # rsi signal
            if self.rsi_signal():
                self.rsi_triggered = True
            # buy
            if self.buy_signal():
                self.buy_all()

            # sell
            if self.stop_loss_signal() or self.take_profit_signal():
                self.sell_all()

        # end of time
        self.candlestick = df.iloc[-1]  # last candle stick
        self.sell_all()
        print(f"MONEY: {self.dollars} $$$")
        Trade.calculate_investment_return()
