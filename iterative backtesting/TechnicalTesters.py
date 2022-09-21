from BaseTester import *
from scipy.signal import argrelextrema

class ConTester(BaseTester):
    '''
    Backtesting class for Contrarian strategies.
    
    Attributes
    ----------
    window: int
        period of simple moving average
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, window):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.window = window
        
    def test_strategy(self):
        self.pre_test_cleanup('Contrarian (window: {})'.format(self.window))
        self.data["returns"] = np.log(self.data['price'] / self.data['price'].shift(1))
        self.data['sign'] = np.sign(self.data['returns'].rolling(self.window).mean())
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['sign'].iloc[bar] < 0:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1  
            elif self.data["sign"].iloc[bar] > 0: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
        self.close_pos(bar+1) # close position at the last bar


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


class EMATester(BaseTester):
    '''
    Backtesting class for EMA crossover strategies.
    
    Attributes
    ----------
    EMA_S: int
        shorter period of exponential moving average
    span_S: float
        shorter period decay in terms of span
    EMA_L: int
        longer period of exponential moving average
    span_L: float
        longer period decay in terms of span
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, EMA_S, span_S, EMA_L, span_L):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.EMA_S = EMA_S
        self.span_S = span_S
        self.EMA_L = EMA_L
        self.span_L = span_L
        
    def test_strategy(self):
        self.pre_test_cleanup('EMA (S: {}, span_S: {}, L: {}, span_L: {})'.format(self.EMA_S, self.span_S, self.EMA_L, self.span_L))
        
        self.data["EMA_S"] = self.data["price"].ewm(span=self.span_S, min_periods=self.EMA_S).mean()
        self.data["EMA_L"] = self.data["price"].ewm(span=self.span_L, min_periods=self.EMA_L).mean()
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data["EMA_S"].iloc[bar] > self.data["EMA_L"].iloc[bar]:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1  
            elif self.data["EMA_S"].iloc[bar] < self.data["EMA_L"].iloc[bar]: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
        self.close_pos(bar+1) # close position at the last bar


class MACDTester(EMATester):
    '''
    Backtesting class for MACD strategies.
    
    Attributes
    ----------
    EMA_S: int
        shorter period of exponential moving average
    span_S: float
        shorter period decay in terms of span
    EMA_L: int
        longer period of exponential moving average
    span_L: float
        longer period decay in terms of span
    signal_period: int
        period for exponential moving average of MACD
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, EMA_S, span_S, EMA_L, span_L, signal_period):
        super().__init__(data, symbol, start, end, amount, use_spread, EMA_S, span_S, EMA_L, span_L)
        self.signal_period = signal_period
        
    def test_strategy(self):
        self.pre_test_cleanup('MACD (S: {}, span_S: {}, L: {}, span_L: {}, signal: {})'.format(self.EMA_S, self.span_S, self.EMA_L, self.span_L, self.signal_period))
        
        self.data["EMA_S"] = self.data["price"].ewm(span=self.span_S, min_periods=self.EMA_S).mean()
        self.data["EMA_L"] = self.data["price"].ewm(span=self.span_L, min_periods=self.EMA_L).mean()
        self.data['MACD'] = self.data['EMA_S'] - self.data['EMA_L']
        self.data['MACD_signal'] = self.data['MACD'].ewm(span=self.signal_period, min_periods=self.signal_period).mean()
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['MACD'].iloc[bar] > self.data['MACD_signal'].iloc[bar]:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1
            elif self.data["MACD"].iloc[bar] < self.data["MACD_signal"].iloc[bar]: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
        self.close_pos(bar+1) # close position at the last bar


class BollingerTester(BaseTester):
    '''
    Backtesting class for Bollinger Bands strategies.
    
    Attributes
    ----------
    SMA: int
        period for simple moving average
    num_sd: int
        number of standard deviations from SMA
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, SMA, num_sd):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.SMA = SMA
        self.num_sd = num_sd
        
    def test_strategy(self):
        self.pre_test_cleanup('Bollinger (SMA: {}, sd: {})'.format(self.SMA, self.num_sd))
        
        self.data["SMA"] = self.data["price"].rolling(self.SMA).mean()
        self.data['Lower'] = self.data['SMA'] - self.data['price'].rolling(self.SMA).std() * self.num_sd
        self.data['Upper'] = self.data['SMA'] + self.data['price'].rolling(self.SMA).std() * self.num_sd
        self.data['distance'] = self.data['price'] - self.data['SMA']
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['price'].iloc[bar] < self.data['Lower'].iloc[bar]:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1
            elif self.data["price"].iloc[bar] > self.data["Upper"].iloc[bar]: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
            elif self.data['distance'].iloc[bar] * self.data['distance'].shift(1).iloc[bar] < 0 or self.data['distance'].shift(1).iloc[bar] is np.nan:
                if self.position != 0:
                    self.close_pos(bar)
                    self.position = 0
                    
        self.close_pos(bar+1) # close position at the last bar


class RSITester(BaseTester):
    '''
    Backtesting class for Relative Strength Indicator strategies.
    
    Attributes
    ----------
    SMA: int
        period for simple moving average
    upper: int
        upper RSI threshold to indicate overbuying (0-100)
    lower: int
        lower RSI threshold to indicate overselling (0-100)
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, SMA, upper, lower):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.SMA = SMA
        self.upper = upper
        self.lower = lower
        
    def test_strategy(self):
        self.pre_test_cleanup('RSI (SMA: {}, upper: {}, lower: {})'.format(self.SMA, self.upper, self.lower))
        
        self.data['upper'] = np.where(self.data['price'].diff() > 0, self.data['price'].diff(), 0)
        self.data['lower'] = np.where(self.data['price'].diff() < 0, -self.data['price'].diff(), 0)
        self.data['MA_upper'] = self.data['upper'].rolling(self.SMA).mean()
        self.data['MA_lower'] = self.data['lower'].rolling(self.SMA).mean()
        self.data['RSI'] = self.data['MA_upper']/(self.data['MA_upper'] + self.data['MA_lower']) * 100
        
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['RSI'].iloc[bar] < self.lower:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1
            elif self.data['RSI'].iloc[bar] > self.upper: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1
            else:
                self.close_pos(bar)
                self.position = 0
                    
        self.close_pos(bar+1) # close position at the last bar


class StochOscTester(BaseTester):
    '''
    Backtesting class for Stochastic Oscillator strategies.
    
    Attributes
    ----------
    fast: int
        period of simple moving average to obtain fast stochastic oscillator (%K line)
    slow: int
        period of simple moving average to obtain slow stochastic oscillator (%D line)
    raw: DataFrame object
        columns = [open, high, low, close, spread], index = date
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, fast, slow):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.fast = fast
        self.slow = slow
        
    def get_values(self, bar):
        '''
        Use closing price in trade
        '''
        date = str(self.data.index[bar].date())
        price = round(self.data.close.iloc[bar], 5)
        spread = round(self.data.spread.iloc[bar], 5)
        return date, price, spread
        
    def test_strategy(self):
        self.pre_test_cleanup('Stochastic Oscillator (fast: {}, slow: {})'.format(self.fast, self.slow))
        
        self.data['roll_low'] = self.data['low'].rolling(fast).mean()
        self.data['roll_high'] = self.data['high'].rolling(fast).mean()
        self.data['K'] = (self.data['close'] - self.data['roll_low'])/(self.data['roll_high'] - self.data['roll_low']) * 100
        self.data['D'] = self.data['K'].rolling(slow).mean()
        
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['K'].iloc[bar] > self.data['D']:
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1
            elif self.data['K'].iloc[bar] < self.data['D']: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = "all") 
                    self.position = -1

        self.close_pos(bar+1) # close position at the last bar


class PivotPointTester(BaseTester):
    '''
    Backtesting class for Pivot Point strategies.
    
    Attributes
    ----------
    raw: DataFrame object
        columns = [open, high, low, close, open_d, high_d, low_d, close_d, spread], index = date
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread):
        super().__init__(data, symbol, start, end, amount, use_spread)
        
    def get_values(self, bar):
        '''
        Use opening price in trade
        '''
        date = str(self.data.index[bar].date())
        price = round(self.data.open.iloc[bar], 5)
        spread = round(self.data.spread.iloc[bar], 5)
        return date, price, spread
        
    def test_strategy(self):
        self.pre_test_cleanup('Pivot Point')
        
        self.data['PP'] = (self.data['high_d'] + self.data['low_d'] + self.data['close_d'])/3
        self.data['S'] = self.data['PP']*2 - self.data['high_d']
        self.data['R'] = self.data['PP']*2 - self.data['low_d']
        
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['open'].iloc[bar] >= self.data['R']:
                if self.position != 0:
                    self.close_pos(bar)
                    self.position = 0
            elif self.data['open'].iloc[bar] > self.data['PP']: 
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") 
                    self.position = 1
            elif self.data['open'].iloc[bar] <= self.data['S']:
                if self.position != 0:
                    self.close_pos(bar)
                    self.position = 0
            elif self.data['open'] < self.data['PP']:
                if self.position in [0, 1]:
                    self.go_short(bar, amount = 'all')
                    self.position = -1

        self.close_pos(bar+1) # close position at the last bar


class FibRetracementTester(BaseTester):
    '''
    Backtesting class for Fibonacci Retracement strategies.
    
    Attributes
    ----------
    fib1: float
        Fibonacci number 1 (0-1)
    fib2: float
        Fibonacci number 2 (0-1)
    order: int
        number of days within a local window
    raw: DataFrame object
        columns = [open, high, low, close, spread], index = date
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread, fib1, fib2, order):
        super().__init__(data, symbol, start, end, amount, use_spread)
        self.fib1 = fib1
        self.fib2 = fib2
        self.order = order
        
    def get_values(self, bar):
        '''
        Use closing price in trade
        '''
        date = str(self.data.index[bar].date())
        price = round(self.data.close.iloc[bar], 5)
        spread = round(self.data.spread.iloc[bar], 5)
        return date, price, spread
        
    def test_strategy(self):
        self.pre_test_cleanup('Fibonacci Retracement (fib1: {}, fib2: {}, order: {})'.format(self.fib1, self.fib2, self.order))
        
        # Local highs
        self.data['hh'], self.data['hh_date'] = np.nan. np.nan
        for bar in range(len(self.data)):
            date = self.data.index[bar]
            hh = self.data.iloc[:bar+1]['high']
            local_max = argrelextrema(hh.values, np.greater_equal, order=self.order)
            self.data.loc[date, 'hh'] = self.data['high'].values[local_max][-1]
            self.data.loc[date, 'hh_date'] = self.data.index[local_max][-1]
        
        # Local lows
        self.data['ll'], self.data['ll_date'] = np.nan. np.nan
        for bar in range(len(self.data)):
            date = self.data.index[bar]
            ll = self.data.iloc[:bar+1]['low']
            local_min = argrelextrema(ll.values, np.less_equal, order=self.order)
            self.data.loc[date, 'll'] = self.data['low'].values[local_min][-1]
            self.data.loc[date, 'll_date'] = self.data.index[local_min][-1]
            
        self.data['trend'] = np.where(self.data['hh_date'] > self.data['ll_date'], 1, -1)
        fib1_col = 'F_{}'.format(self.fib1 * 100)
        fib2_col = 'F_{}'.format(self.fib2 * 100)
        self.data[fib1_col] = np.where(self.data['trend'] == 1,
                                                            self.data['hh'] - (self.data['hh']-self.data['ll'])*self.fib1,
                                                            self.data['hh'] - (self.data['hh']-self.data['ll'])*(1 - self.fib1))
        self.data[fib2_col] = np.where(self.data['trend'] == 1,
                                                            self.data['hh'] - (self.data['hh']-self.data['ll'])*self.fib2,
                                                            self.data['hh'] - (self.data['hh']-self.data['ll'])*(1 - self.fib2))
        
        self.data.dropna(inplace = True)

        for bar in range(len(self.data)-1): # all bars (except the last bar)
            if self.data['hh'].iloc[bar] != self.data['hh'].shift().iloc[bar] or                     self.data['ll'].iloc[bar] != self.data['ll'].shift().iloc[bar]:
                if self.position != 0:
                    self.close_pos(bar) # neutral when trend reverses/new local high or lows reached
                    self.position = 0
            # Downtrend
            elif self.data['trend'].iloc[bar] == -1 and                     self.data['close'].shift().iloc[bar] > self.data[ll].shift().iloc[bar] and                     self.data['close'].iloc[bar] <= self.data[ll].iloc[bar]: 
                if self.position != 0:
                    self.close_pos(bar) # neutral when price drops below local min on downtrend, stop loss
                    self.position = 0
            elif self.data['trend'].iloc[bar] == -1 and                     self.data['close'].shift().iloc[bar] < self.data[fib2_col].shift().iloc[bar] and                     self.data['close'].iloc[bar] >= self.data[fib2_col].iloc[bar]: 
                if self.position != 0:
                    self.close_pos(bar) # neutral when price reaches R2 on downtrend, take profit
                    self.position = 0
            elif self.data['trend'].iloc[bar] == -1 and                     self.data['close'].shift().iloc[bar] < self.data[fib1_col].shift().iloc[bar] and                     self.data['close'].iloc[bar] > self.data[fib1_col].iloc[bar]: 
                if self.position in [0, -1]:
                    self.go_long(bar, amount = "all") # long when price breaks R1 on downtrend
                    self.position = 1
            
            # Uptrend
            elif self.data['trend'].iloc[bar] == 1 and                     self.data['close'].shift().iloc[bar] < self.data[hh].shift().iloc[bar] and                     self.data['close'].iloc[bar] >= self.data[hh].iloc[bar]: 
                if self.position != 0:
                    self.close_pos(bar) # neutral when price goes above local max on uptrend, stop loss
                    self.position = 0
            elif self.data['trend'].iloc[bar] == 1 and                     self.data['close'].shift().iloc[bar] > self.data[fib2_col].shift().iloc[bar] and                     self.data['close'].iloc[bar] <= self.data[fib2_col].iloc[bar]: 
                if self.position != 0:
                    self.close_pos(bar) # neutral when price reaches S2 on uptrend, take profit
                    self.position = 0
            elif self.data['trend'].iloc[bar] == 1 and                     self.data['close'].shift().iloc[bar] > self.data[fib1_col].shift().iloc[bar] and                     self.data['close'].iloc[bar] < self.data[fib1_col].iloc[bar]: 
                if self.position in [0, 1]:
                    self.go_short(bar, amount = 'all') # short when price breaks S1 on uptrend
                    self.position = -1
                    
        self.close_pos(bar+1) # close position at the last bar

