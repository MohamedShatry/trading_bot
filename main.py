from config import *
from indicators import Indicators
from oandaAPI import Broker

import pandas as pd
import numpy as np

def main():
    oanda = Broker(API_KEY, ACCOUNT_ID)
    position_size = 2000
    pairs = ["EUR_USD", "GBP_USD", "USD_CHF", "AUD_USD", "USD_CAD"]
    upward_sma_dir = {x: False for x in pairs}
    downward_sma_dir = {x: False for x in pairs}

    print("trying")
    open_trades = oanda.get_open_trades()
    curr_ls = []

    for i in range(len(open_trades)):
        curr_ls.append(open_trades[i]['instrument'])

    currencies = [i for i in pairs if i not in curr_ls]

    # Look to see if it's a good time to buy a new pair
    for currency in currencies:
        data = oanda.get_candles(currency)
        technicals = Indicators(data)
        ohlc_df = technicals.stochastic(data)
        ohlc_df = technicals.SMA(ohlc_df)

        signal = oanda.trade_signal(
            ohlc_df, currency, upward_sma_dir, downward_sma_dir)

        if signal == "Buy":
            oanda.make_order(currency, position_size,
                             3*technicals.ATR(ohlc_df))
            print("New long position initiated for ", currency)

    # Look to see if it's a good time to sell a pair:
    for currency in curr_ls:
        data = oanda.get_candles(currency)
        technicals = Indicators(data)
        ohlc_df = technicals.stochastic(data)
        ohlc_df = technicals.SMA(ohlc_df)

        signal = oanda.trade_signal(
            ohlc_df, currency, upward_sma_dir, downward_sma_dir)

        if signal == "Sell":
            oanda.make_order(currency, -1*position_size,
                             3*technicals.ATR(ohlc_df))
            print("New short position initiated for ", currency)


if __name__ == "__main__":
    main()
