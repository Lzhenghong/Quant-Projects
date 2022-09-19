from BaseTester import *

class SMATester(BaseTester):
    '''
    Backtesting class for SMA crossover strategies.
    
    Attributes
    ----------
    SMA_S: int
        shorter period of simple moving average
    SMA_L: int
        longer period of simple moving average
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, SMA_S, SMA_L):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        
    def test_strategy(self):
        self.pre_test_cleanup('SMA (S: {}, L: {})'.format(self.SMA_S, self.SMA_L))
        
        self.data["SMA_S"] = self.data["price"].rolling(self.SMA_S).mean()
        self.data["SMA_L"] = self.data["price"].rolling(self.SMA_L).mean()
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data["SMA_S"].iloc[bar] > self.data["SMA_L"].iloc[bar]:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1  
            elif self.data["SMA_S"].iloc[bar] < self.data["SMA_L"].iloc[bar]: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
        self.close_pos(bar+1) # close position at the last bar

