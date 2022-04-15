from models.candlestick import Candlestick
from models.trade import Trade
from trader import Trader
import math


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
                 interval="5m",
                 qty_increment_decimal_points=4) -> None:
        super().__init__(clear_db,
                         update_db,
                         dollars,
                         starting_asset,
                         take_profit_ratio,
                         stop_loss_ratio,
                         rsi_threshold,
                         ticker,
                         period,
                         interval,
                         qty_increment_decimal_points)

        Trade.clear_table()
        self.data = Candlestick.get_processed_candlesticks()
        self.run_historical_simulation()
        self.print_stats()

    def buy_all(self) -> bool:

        buy_price = self.candlestick["close"]
        self.quantity = self.round_quantity_down(self.dollars/buy_price)
        # substruct what we paied for the asset
        self.dollars -= self.quantity*buy_price

        self.current_trade = Trade.create(buy_price=buy_price,
                                          quantity=self.quantity,
                                          buy_datetime=self.candlestick['datetime'])

        return True

    def sell_all(self) -> bool:

        price_for_asset = self.candlestick["close"]
        self.dollars += self.quantity*price_for_asset
        self.quantity = 0
        self.current_trade.sell_datetime = self.candlestick['datetime']
        self.current_trade.sell_price = price_for_asset
        self.current_trade.save()

        self.reset_variables()
        return True

    def run_historical_simulation(self):

        df = self.data.reset_index()
        for _, candlestick in df.iterrows():
            self.candlestick = candlestick
            self.take_action()

        # end of time
        self.candlestick = df.iloc[-1]  # last candle stick
        self.sell_all()
        print(f"MONEY: {self.dollars} $$$")
