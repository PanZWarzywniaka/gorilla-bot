import pandas as pd
import pandas_ta as ta


class CandlestickProcessor(object):
    def __init__(self, data: pd.DataFrame,
                 rsi_length=14,
                 macd_fast=12,
                 macd_slow=26,
                 macd_signal=9) -> None:

        self.data = data
        self.rsi_length = rsi_length
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.__process_data()

    @property
    def processed_data(self) -> pd.DataFrame:
        return self.data

    def __process_data(self):

        self.__calculate_rsi()
        self.__calculate_macd()
        pd.set_option("display.max_columns", None)
        self.data.columns = self.data.columns.str.lower()
        self.data.index.name = 'datetime'

    def __calculate_rsi(self):
        self.data.ta.rsi(close='close', length=self.rsi_length, append=True)
        self.data.rename(
            columns={f'RSI_{self.rsi_length}': 'RSI'}, inplace=True)

    def __calculate_macd(self):
        fast = self.macd_fast
        slow = self.macd_slow
        signal = self.macd_signal

        self.data.ta.macd(close='close',
                          fast=fast,
                          slow=slow,
                          signal=signal,
                          append=True)

        self.data.rename(
            columns={
                f'MACD_{fast}_{slow}_{signal}': 'macd_fast',
                f'MACDs_{fast}_{slow}_{signal}': 'macd_slow',
                f'MACDh_{fast}_{slow}_{signal}': 'macd_hist',

            }, inplace=True)

        self.data['macd_above'] = self.data['macd_fast'] >= self.data['macd_slow']
        self.data['macd_crossover'] = self.data['macd_above'].diff()
