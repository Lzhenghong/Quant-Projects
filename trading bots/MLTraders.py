from BaseTrader import BaseTrader
import pandas as pd
import numpy as np


class MLTrader(BaseTrader):
    '''
    Trader class using fitted Machine Learning.
    
    Attributes
    ----------
    lags: int
        number of lags to fit input into model
    model: object
        machine learning model
    '''
    def __init__(self, conf_file, instrument, bar_length, units, stop, lags, model):
        super().__init__(conf_file, instrument, bar_length, units, stop)
        self.lags = lags
        self.model = model
        
    def define_strategy(self):
        '''
        Predict position based on lagged returns.
        '''
        df = self.raw_data.copy()
        
        df = df.append(self.tick_data)
        df["returns"] = np.log(df[self.instrument] / df[self.instrument].shift())
        cols = []
        for lag in range(1, self.lags + 1):
            col = "lag{}".format(lag)
            df[col] = df.returns.shift(lag)
            cols.append(col)
        df.dropna(inplace = True)
        df["position"] = self.model.predict(df[cols])
        
        self.data = df.copy()