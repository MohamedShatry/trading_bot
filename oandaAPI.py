import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd
import numpy as np


class Broker():

    def __init__(self, key, account_number):
        self.key = key
        self.account_num = account_number
        self.client = oandapyV20.API(access_token=key, environment="practice")

    def get_candles(self, pair):
        params = {"count": 800, "granularity": "M15"}
        candles = instruments.InstrumentsCandles(
            instrument=pair, params=params)
        self.client.request(candles)
        ohlc_dict = candles.response["candles"]
        ohlc = pd.DataFrame(ohlc_dict)
        ohlc_df = ohlc.mid.dropna().apply(pd.Series)
        ohlc_df["volume"] = ohlc["volume"]
        ohlc_df.index = ohlc["time"]
        ohlc_df = ohlc_df.apply(pd.to_numeric)
        ohlc_df.columns = ["open", "high", "low", "close", "volume"]
        return ohlc_df

    def make_order(self, pair, units, stop_loss):
        """units can be positive or negative, stop loss (in pips) added/subtracted to price """
        data = {
            "order": {
                "price": "",
                "stopLossOnFill": {
                    "trailingStopLossOnFill": "GTC",
                    "distance": str(stop_loss)
                },
                "timeInForce": "FOK",
                "instrument": str(pair),
                "units": str(units),
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        r = orders.OrderCreate(accountID=self.account_num, data=data)
        self.client.request(r)

    def trade_signal(self, df, pair, upward_sma_dir, downward_sma_dir):
        "function to generate signal"
        signal = ""

        if df['sma_fast'][-1] > df['sma_slow'][-1] and df['sma_fast'][-2] < df['sma_slow'][-2]:
            upward_sma_dir[pair] = True
            downward_sma_dir[pair] = False
        if df['sma_fast'][-1] < df['sma_slow'][-1] and df['sma_fast'][-2] > df['sma_slow'][-2]:
            upward_sma_dir[pair] = False
            downward_sma_dir[pair] = True

        print(downward_sma_dir)
        if upward_sma_dir[pair] == True and min(df['K'][-1], df['D'][-1]) > 25 and max(df['K'][-2], df['D'][-2]) < 25:
            signal = "Buy"
        if downward_sma_dir[pair] == True and min(df['K'][-1], df['D'][-1]) > 75 and max(df['K'][-2], df['D'][-2]) < 75:
            signal = "Sell"

        print("In signal " + signal)
        return signal

    def get_open_trades(self):
        r = trades.OpenTrades(accountID=self.account_num)
        open_trades = self.client.request(r)['trades']
        return open_trades
