import pandas as pd
import numpy as np


class Indicators():

    def __init__(self, DF):
        self.df = DF

    def stochastic(self, df, a=14, b=3, c=3):
        "function to calculate stochastic"
        df['k'] = ((df['close'] - df['low'].rolling(a).min()) /
                   (df['high'].rolling(a).max()-df['low'].rolling(a).min()))*100
        df['K'] = df['k'].rolling(b).mean()
        df['D'] = df['K'].rolling(c).mean()
        return df

    def SMA(self, df, a=100, b=100):
        "function to calculate stochastic"
        df['sma_fast'] = df['close'].rolling(a).mean()
        df['sma_slow'] = df['close'].rolling(b).mean()
        return df

    def ATR(self, df, n=120):
        "function to calculate True Range and Average True Range"
        df['H-L'] = abs(df['high']-df['low'])
        df['H-PC'] = abs(df['high']-df['close'].shift(1))
        df['L-PC'] = abs(df['low']-df['close'].shift(1))
        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
        df['ATR'] = df['TR'].rolling(n).mean()
        df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
        df2
        return round(df2["ATR"][-1], 2)
