from datetime import datetime
from historical_trader import HistoricalTrader
from live_trader import LiveTrader


def main():
    ticker = "BCH-USD"
    interval = "5m"
    qty_increment_decimal_points = 4
    trader = HistoricalTrader(
        clear_db=True,
        update_db=True,  # downloads candle sticks from the internet
        dollars=100,
        starting_asset=0,

        # as percent of entry money
        take_profit_ratio=3,
        stop_loss_ratio=1,
        rsi_threshold=30,

        ticker=ticker,
        period="7d",
        interval=interval,
        qty_increment_decimal_points=qty_increment_decimal_points
    )

    trader.make_charts(
        # start=datetime(2022, 4, 2),
        # end=datetime(2022, 4, 6),
    )
    # trader = LiveTrader(api_key_id="PKC5LZY4HEJ9BL9EGHXE",
    #                     api_secret_key="gJsV346k4dhS65hvWvj58Knlb5wfgMLjLPgGTeNZ",
    #                     api_url='https://paper-api.alpaca.markets',
    #                     dollars=100, starting_asset=0,
    #                     take_profit_ratio=3, stop_loss_ratio=1, rsi_threshold=30,
    #                     ticker=ticker, historic_data_period="60d", interval=interval,
    #                     qty_increment_decimal_points=qty_increment_decimal_points)


if __name__ == '__main__':
    main()
