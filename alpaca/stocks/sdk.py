# core
import json
import datetime
# 3rd party
import numpy as np
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import alpaca_trade_api

# own

from trader import Data

# def print_bar(bar: alpaca_trade_api.entity.Bar):
#     print("\nBAR")
#     print(f"Time stamp: {bar.t}")

#     print(f"Open: {bar.o}")
#     print(f"Close: {bar.c}")
#     print(f"Gain: {bar.c-bar.o}")
#     print(f"High: {bar.h}")
#     print(f"Low: {bar.l}")
#     print()


# def get_score(data, lastn):

#     return get_diff(data, lastn)/get_variance(data)


# def get_variance(bars):

#     prices = bars['close'].array
#     return np.std(prices)


# def get_diff(bars, lastn):

#     start = bars.iloc[-lastn]['open']  # first open
#     end = bars.iloc[-1]['close']  # last close
#     diff = (end-start)  # *100  # % gain
#     return diff


# def get_bars_of_asset(api, asset):
#     return api.get_bars(asset.symbol, TimeFrame.Minute, "2022-01-06",
#                         "2022-01-12", adjustment='raw').df


# def get_score_of_asset(api, asset):

#     if asset.status == 'inactive':
#         return
#     bars = get_bars_of_asset(api, asset)

#     LAST_N = 20
#     if len(bars) < LAST_N:
#         return
#     print(f"Calculating score for {asset.symbol}. Got {len(bars)} entries.")
#     return get_score(bars, LAST_N)


def main():
    d = Data(1000, TimeFrame(1, TimeFrameUnit.Minute),
             20, "2022-01-06", "2022-01-12")
    d.get_data()
    print(d.prices)
    with open('result.json', 'w') as fp:
        json.dump(d.prices, fp)


if __name__ == '__main__':
    main()
