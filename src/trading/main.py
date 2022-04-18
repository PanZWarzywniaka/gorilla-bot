from datetime import datetime
from historical_trader import HistoricalTrader
from live_trader import LiveTrader
from util.visualizer import Visualizer


def main():
    ticker = "BCH-USD"
    interval = "5m"
    qty_increment_decimal_points = 4
    trader = HistoricalTrader(
        clear_db=True,
        update_db=True,  # downloads candle sticks from the internet
        dollars=100,
        starting_quantity=0,

        # as percent of entry money
        take_profit_ratio=2,
        stop_loss_ratio=1,
        rsi_threshold=30,

        ticker=ticker,
        period="60d",
        interval=interval,
        qty_increment_decimal_points=qty_increment_decimal_points
    )
    Visualizer()

    # trader = LiveTrader(api_key_id="PKD0O8AYXYV6KT363ZCY",
    #                     api_secret_key="KJdYuQCd6OU2olYIEJrpOhgoGhb4T8AzJTNdlWrz",
    #                     api_url='https://paper-api.alpaca.markets',
    #                     dollars=100, starting_quantity=0,
    #                     take_profit_ratio=2, stop_loss_ratio=1, rsi_threshold=30,
    #                     ticker=ticker, historic_data_period="60d", interval=interval,
    #                     qty_increment_decimal_points=qty_increment_decimal_points)


if __name__ == '__main__':
    main()
