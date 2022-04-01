from trader import Trader
from models.trade import Trade


class HistoricalTrader(Trader):
    def __init__(self,
                 dollars=100,
                 starting_asset=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m") -> None:
        super().__init__(dollars,
                         starting_asset,
                         take_profit_ratio,
                         stop_loss_ratio,
                         rsi_threshold,
                         ticker,
                         period,
                         interval)
        self.main_loop()

    def main_loop(self):
        pass
