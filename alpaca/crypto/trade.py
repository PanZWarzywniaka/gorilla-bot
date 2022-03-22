

class Trade():
    def __init__(self, rsi_signal_time) -> None:

        self.rsi_signal_time = rsi_signal_time

        self.buy_time = None
        self.sell_time = None

        self.buy_price = None
        self.sell_price = None

        self.current_take_profit = None
        self.current_stop_loss = None
