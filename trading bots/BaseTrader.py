#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tpqoa
from datetime import datetime, timedelta
import time


# In[ ]:


class BaseTrader(tpqoa.tpqoa):
    '''
    Base trader class to execute trades on OANDA
    
    Attributes
    ----------
    conf_file: str
        directory of configuration file containining OANDA account ID and access token
    instrument: str
        financial instrument to be traded
    bar_length: int
        minimum duration between trades
    tick_data: Pandas Dataframe
        contains newly streamed data for price of instrument within bar_length
    raw_data: Pandas Dataframe
        contains historical data for price of instrument
    data: Pandas Dataframe
        contains returns, position and other strategy-specific attributes
    last_bar: datetime
        time of last record in raw_data
    units: int
        number of units traded
    position: int
        -1 for short, 0 for neutral, 1 for long
    profits: list
        stores trade profits each time position changes
    stop: str
        time to stop trading session, in HH:MM format
    '''
    def __init__(self, conf_file, instrument, bar_length, units, stop):
        super().__init__(conf_file)
        self.instrument = instrument
        self.bar_length = pd.to_timedelta(bar_length)
        self.tick_data = pd.DataFrame()
        self.raw_data = None
        self.data = None 
        self.last_bar = None
        self.units = units
        self.position = 0
        self.profits = []
        self.stop = stop
    
    def get_most_recent(self, days = 5):
        '''
        Retrieves most recent price data.
            
            Parameters:
                days (int): number of days previously to retrieve data from
        '''
        while True:
            time.sleep(2)
            now = datetime.utcnow()
            now = now - timedelta(microseconds = now.microsecond)
            past = now - timedelta(days = days)
            df = self.get_history(instrument = self.instrument, start = past, end = now,
                                   granularity = "S5", price = "M", localize = False).c.dropna().to_frame()
            df.rename(columns = {"c":self.instrument}, inplace = True)
            df = df.resample(self.bar_length, label = "right").last().dropna().iloc[:-1]
            self.raw_data = df.copy()
            self.last_bar = self.raw_data.index[-1]
            if pd.to_datetime(datetime.utcnow()).tz_localize("UTC") - self.last_bar < self.bar_length:
                break
                
    def on_success(self, time, bid, ask):
        '''
        Called by tpqoa's stream_data() function. Calculates half price, samples data and execute 
        trades if time elapsed since last record exceeds bar_length.
        
            Parameters:
                time (string): current time
                bid (int): bid price of instrument
                ask (int): offer price of instrument
        '''
        print(self.ticks, end = " ", flush = True)
        
        recent_tick = pd.to_datetime(time)
        if recent_tick.time() >= pd.to_datetime(self.stop).time():
            self.stop_stream = True
            
        df = pd.DataFrame({self.instrument:(ask + bid)/2}, 
                          index = [recent_tick])
        self.tick_data = self.tick_data.append(df)
        
        if recent_tick - self.last_bar > self.bar_length:
            self.resample_and_join()
            self.define_strategy()
            self.execute_trades()
    
    def resample_and_join(self):
        '''
        Appends tick_data except last record to raw_data as previous bar. 
        Last tick_data is first record of new bar.
        '''
        self.raw_data = self.raw_data.append(self.tick_data.resample(self.bar_length, 
                                                                  label="right").last().ffill().iloc[:-1])
        self.tick_data = self.tick_data.iloc[-1:]
        self.last_bar = self.raw_data.index[-1]
    
    def define_strategy(self):
        pass
    
    def execute_trades(self):
        pass
    
    def report_trade(self, order, going):
        '''
        Prints trade records.
        
        Parameters:
            order(Dataframe): dataframe containing time, units, price and P&L
            going (str): new position
        '''
        time = order["time"]
        units = order["units"]
        price = order["price"]
        pl = float(order["pl"])
        self.profits.append(pl)
        cumpl = sum(self.profits)
        print("\n" + 100* "-")
        print("{} | {}".format(time, going))
        print("{} | units = {} | price = {} | P&L = {} | Cum P&L = {}".format(time, units, price, pl, cumpl))
        print(100 * "-" + "\n")  

