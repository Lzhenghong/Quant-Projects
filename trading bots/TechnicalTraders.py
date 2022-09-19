from BaseTrader import BaseTrader
import pandas as pd
import numpy as np

class ConTrader(BaseTrader):
    '''
    Trader class using Contrarian strategy.
    
    Attributes
    ----------
    window: int
        period of simple moving average
    '''
    def __init__(self, conf_file, instrument, bar_length, units, window):
        super().__init__(conf_file, instrument, bar_length, units)
        self.window = window
        
    def define_strategy(self): # "strategy-specific"
        '''
        Go long if simple moving average returns are decreasing.
        Go short if returns are increasing.
        Go neutral if returns are unchanged.
        '''
        df = self.raw_data.copy()
        df["returns"] = np.log(df[self.instrument] / df[self.instrument].shift())
        df["position"] = -np.sign(df.returns.rolling(self.window).mean())
        self.data = df.copy()
        

class SMATrader(BaseTrader):
    '''
    Trader class using short and long simple moving averages.
    
    Attributes
    ----------
    SMA_S: int
        shorter period for simple moving average
    SMA_L: int
        longer period for simple moving average
    '''
    def __init__(self, conf_file, instrument, bar_length, units, SMA_S, SMA_L):
        super().__init__(conf_file, instrument, bar_length, units)
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        
    def define_strategy(self):
        '''
        Go long if SMA_S goes above SMA_L. 
        Go short if SMA_S goes below SMA_L.
        '''
        df = self.raw_data.copy()
        df["SMA_S"] = df[self.instrument].rolling(self.SMA_S).mean()
        df["SMA_L"] = df[self.instrument].rolling(self.SMA_L).mean()
        df["position"] = np.where(df["SMA_S"] > df["SMA_L"], 1, -1)
        self.data = df.copy()
        

class EMATrader(BaseTrader):
    '''
    Trader class using short and long exponential moving averages.
    
    Attributes
    ----------
    EMA_S: int
        shorter period for exponential moving average
    span_S: float
        shorter period decay in terms of span
    EMA_L: int
        longer period for exponential moving average
    span_L: float
        longer period decay in terms of span
    '''
    def __init__(self, conf_file, instrument, bar_length, units, EMA_S, span_S, EMA_L, span_L):
        super().__init__(conf_file, instrument, bar_length, units)
        self.EMA_S = EMA_S
        self.span_S = span_S
        self.EMA_L = EMA_L
        self.span_L = span_L
        
    def define_strategy(self):
        '''
        Go long if EMA_S goes above EMA_L. 
        Go short if EMA_S goes below EMA_L.
        '''
        df = self.raw_data.copy()
        df["EMA_S"] = df[self.instrument].ewm(span=span_S, min_periods=self.EMA_S).mean()
        df["EMA_L"] = df[self.instrument].ewm(span=span_L, min_periods=self.EMA_L).mean()
        df["position"] = np.where(df["EMA_S"] > df["EMA_L"], 1, -1)
        self.data = df.copy()
        

class BollingerTrader(BaseTrader):
    '''
    Trader class using Bollinger Bands.
    
    Attributes
    ----------
    SMA: int
        period for simple moving average
    num_sd: int
        number of standard deviations from SMA
    '''
    def __init__(self, conf_file, instrument, bar_length, units, SMA, num_sd):
        super().__init__(conf_file, instrument, bar_length, units)
        self.SMA = SMA
        self.num_sd = num_sd
        
    def define_strategy(self):
        '''
        Go long if price goes below support level.
        Go short if price goes above resistance level.
        Go neutral if price crosses SMA.
        Maintain previous position otherwise.
        '''
        df = self.raw_data.copy()
        
        df["SMA"] = df[self.instrument].rolling(self.SMA).mean()
        df["Lower"] = df["SMA"] - df[self.instrument].rolling(self.SMA).std() * self.num_sd
        df["Upper"] = df["SMA"] + df[self.instrument].rolling(self.SMA).std() * self.num_sd
        df["distance"] = df[self.instrument] - df.SMA
        df["position"] = np.where(df[self.instrument] < df.Lower, 1, np.nan)
        df["position"] = np.where(df[self.instrument] > df.Upper, -1, df["position"])
        df["position"] = np.where(df.distance * df.distance.shift(1) < 0, 0, df["position"])
        df["position"] = df.position.ffill().fillna(0)
        
        self.data = df.copy()
        

class MACDTrader(EMATrader):
    '''
    Trader class using Moving Average Convergence Divergence.
    
    Attributes
    ----------
    EMA_S: int
        shorter period for exponential moving average
    span_S: float
        shorter period decay in terms of span
    EMA_L: int
        longer period for exponential moving average
    span_L: float
        longer period decay in terms of span
    signal_period
        period for exponential moving average of MACD
    '''
    def __init__(self, conf_file, instrument, bar_length, units, EMA_S, span_S, EMA_L, span_L, signal_period):
        super().__init__(conf_file, instrument, bar_length, units, EMA_S, span_S, EMA_L, span_L)
        self.signal_period = signal_period
        
    def define_strategy(self):
        '''
        Go long if MACD goes above MACD signal. 
        Go short if MACD goes below MACD signal.
        '''
        df = self.raw_data.copy()
        df["EMA_S"] = df[self.instrument].ewm(span=span_S, min_periods=self.EMA_S).mean()
        df["EMA_L"] = df[self.instrument].ewm(span=span_L, min_periods=self.EMA_L).mean()
        df['MACD'] = df['EMA_S'] - df['EMA_L']
        df['MACD_signal'] = df['MACD'].ewm(span=self.signal_period, min_periods=self.signal_period).mean()
        
        df["position"] = np.where(df["MACD"] > df["MACD_signal"], 1, -1)
        self.data = df.copy()


class RSITrader(BaseTrader):
    '''
    Trader class using Relative Strength Indicator.
    
    Attributes
    ----------
    SMA: int
        period for simple moving average
    upper: int
        upper RSI threshold to indicate overbuying
    lower: int
        lower RSI threshold to indicate overselling
    '''
    def __init__(self, conf_file, instrument, bar_length, units, SMA, upper, lower):
        super().__init__(conf_file, instrument, bar_length, units)
        self.SMA = SMA
        self.upper = upper
        self.lower = lower
        
    def define_strategy(self):
        '''
        Go long if RSI goes below lower. 
        Go short if RSI goes above upper.
        Go neutral otherwise.
        '''
        df = self.raw_data.copy()
        df['upper'] = np.where(df[self.instrument].diff() > 0, df[self.instrument].diff(), 0)
        df['lower'] = np.where(df[self.instrument].diff() < 0, -df[self.instrument].diff(), 0)
        df['MA_upper'] = df['upper'].rolling(SMA).mean()
        df['MA_lower'] = df['lower'].rolling(SMA).mean()
        df['RSI'] = df['MA_upper']/(df['MA_upper'] + df['MA_lower']) * 100
        df.dropna(inplace=True)
        
        df['position'] = np.where(df['RSI'] > self.upper, -1, np.nan)
        df['position'] = np.where(df['RSI'] < self.lower, 1, df['position'])
        df.fillna(0, inplace=True)
        self.data = df.copy()

