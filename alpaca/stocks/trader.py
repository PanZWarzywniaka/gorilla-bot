# core
import enum
import json
import datetime
import concurrent.futures
# 3rd party
import numpy as np
import alpaca_trade_api
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
# own
from config import init


class Data:

    def __init__(self, min_bar_enties: int, tf: TimeFrame, last_n_entries: int, start: str, end: str) -> None:
        init()
        self.api = REST()
        self.min_bar_enties = min_bar_enties
        self.time_frame = tf
        self.last_n_entries = last_n_entries
        self.prices = {}
        self.start = start
        self.end = end

    def __print_bar(self, bar: alpaca_trade_api.entity.Bar) -> None:
        print("\nBAR")
        print(f"Time stamp: {bar.t}")

        print(f"Open: {bar.o}")
        print(f"Close: {bar.c}")
        print(f"Gain: {bar.c-bar.o}")
        print(f"High: {bar.h}")
        print(f"Low: {bar.l}")
        print()

    def __get_variance(self, bars):
        prices = bars['close'].array
        return np.std(prices)

    def __get_diff(self, bars) -> float:

        start = bars.iloc[-self.last_n_entries]['open']  # first open
        end = bars.iloc[-1]['close']  # last close
        diff = end-start  # *100  # % gain
        return diff

    def __get_score(self, bars) -> float:
        return self.__get_diff(bars) / self.__get_variance(bars)

    def __get_bars_of_asset(self, asset):
        return self.api.get_bars(asset.symbol, self.time_frame,
                                 self.start, self.end, adjustment='raw').df

    def __process_asset(self, asset):
        #print(f"{count+1}/{total_assets} {asset.symbol} ", end='')
        print(f"{asset.symbol} ", end='')
        try:
            bars = self.__get_bars_of_asset(asset)
        except Exception as err:
            print(f"Error: {err.with_traceback}")
            return

        n_entries = len(bars)
        if n_entries < self.min_bar_enties:
            print("not enough data")
            return

        print(f" calculating score for {n_entries} entries: ", end='')
        score = self.__get_score(bars)
        print(score)
        self.prices[asset.symbol] = score

    def get_data(self):
        assets = self.api.list_assets(status='active')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.__process_asset, assets)
