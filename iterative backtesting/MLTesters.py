from BaseTester import *
import pandas as pd
import numpy as np

class MLTester(BaseTester):
    '''
    Backtesting class for Machine Learning strategies
    
    Attributes
    ----------
    lags: int
        number of lags to fit input into model
    model: object
        machine learning model
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, lags, model):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.lags = lags
        self.model = model
    
    def test_strategy(self, model_name):
        self.pre_test_cleanup('Machine Learning (lags: {}, model_name: {})'.format(self.lags, model_name))

        self.data["returns"] = np.log(self.data['price'] / self.data['price'].shift(1))
        cols = []
        for lag in range(1, self.lags + 1):
            col = "lag{}".format(lag)
            self.data[col] = self.data['returns'].shift(lag)
            cols.append(col)

        self.data.dropna(inplace = True)
        self.data["position"] = self.model.predict(self.data[cols])

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['position'].iloc[bar] == 1:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1  
            elif self.data["position"].iloc[bar] == -1: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
            else:
                if self.position != 0:
                    self.close_pos(bar)
                    self.position = 0
        self.close_pos(bar+1) # close position at the last bar

