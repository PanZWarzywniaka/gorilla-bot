from gorilla_bot.models.candlestick import Candlestick
from gorilla_bot.models.trade import Trade
from gorilla_bot.trader import Trader
import math


class HistoricalTrader(Trader):
    def __init__(self,
                 dollars,
                 ticker,
                 period,
                 interval,
                 qty_increment_decimal_points) -> None:
        super().__init__(
            dollars,
            ticker,
            period,
            interval)

        raw_data = Candlestick.download_yahoo_candlestics(
            ticker=ticker, period=period, interval=interval)
        self.data = Candlestick.process_candlesticks(raw_data)

        self.qty_increment_decimal_points = qty_increment_decimal_points

        # start
        self.run_historical_simulation()

    def buy_all(self) -> bool:

        buy_price = self.candlestick["close"]
        self.quantity += self.__round_quantity_down(self.dollars/buy_price)
        # substruct what we paied for the asset
        self.dollars -= self.quantity*buy_price

        self.current_trade = Trade.create(buy_price=buy_price,
                                          quantity=self.quantity,
                                          buy_datetime=self.candlestick['datetime'])

        return True

    def sell_all(self) -> bool:

        price_for_quantity = self.candlestick["close"]
        self.dollars += self.quantity*price_for_quantity
        self.quantity = 0
        self.current_trade.sell_datetime = self.candlestick['datetime']
        self.current_trade.sell_price = price_for_quantity
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
        self.print_stats()

    # ensures that the quantity we want to buy (qty) is up to qty_increment_decimal_points
    def __round_quantity_down(self, qty: float) -> float:
        factor = 10 ** self.qty_increment_decimal_points
        return math.floor(qty * factor) / factor
