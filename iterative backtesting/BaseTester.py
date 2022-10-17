import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

class BaseTester():
    '''
    Base class for iterative/event-driven backtesting of trading strategies.
    
    Attributes
        ----------
        raw: DataFrame Object
            columns = [price, spread], index = date
        data: DataFrame object
            contains other trading information
        symbol: str
            ticker symbol to be backtested
        start: str
            start date
        end: str
            end date
        amount: float
            initial amount to be invested per trade
        use_spread: boolean
            whether trading costs (bid-offer spread) are included
        initial_balance: float
            initial amount in account
        current_balance: float
            current amount in account
        units: int
            number of units held in position
        trades: int
            number of trades executed
        position: int
            -1 for short, 0 for neutral, 1 for long
    '''
    def __init__(self, data, symbol, start, end, amount, use_spread = True, print_log = False):
        self.raw = data
        self.data = None
        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_balance = amount
        self.current_balance = amount
        self.units = 0
        self.trades = 0
        self.position = 0
        self.use_spread = use_spread
        self.print_log = print_log
        
        self.process_data()
    
    def process_data(self):
        ''' 
        Calculate returns of buy-and-hold strategy.
        '''
        temp = self.raw.copy()
        temp = temp.loc[self.start:self.end]
        self.data = temp

    def plot_data(self, cols = None):  
        ''' 
        Plots the closing price for the symbol.
        '''
        if cols is None:
            cols = "price"
        self.data[cols].plot(figsize = (12, 8), title = self.symbol)
    
    def get_values(self, bar):
        ''' 
        Returns the date, the price and the spread for the given bar.
        '''
        date = str(self.data.index[bar].date())
        price = round(self.data.price.iloc[bar], 5)
        spread = round(self.data.spread.iloc[bar], 5)
        return date, price, spread
    
    def print_current_balance(self, bar):
        ''' 
        Prints out the current (cash) balance.
        '''
        date, price, spread = self.get_values(bar)
        if self.print_log:
            print("{} | Current Balance: {}".format(date, round(self.current_balance, 2)))
        
    def buy_instrument(self, bar, units = None, amount = None):
        ''' 
        Places and executes a buy order.
        '''
        date, price, spread = self.get_values(bar)
        if self.use_spread:
            price += spread/2 # offer price
        if amount is not None:
            units = int(amount / price)
        self.current_balance -= units * price 
        self.units += units
        self.trades += 1
        if self.print_log:
            print("{} |  Buying {} for {}".format(date, units, round(price, 5)))
    
    def sell_instrument(self, bar, units = None, amount = None):
        ''' 
        Places and executes a sell order.
        '''
        date, price, spread = self.get_values(bar)
        if self.use_spread:
            price -= spread/2 # bid price
        if amount is not None: 
            units = int(amount / price)
        self.current_balance += units * price
        self.units -= units
        self.trades += 1
        if self.print_log:
            print("{} |  Selling {} for {}".format(date, units, round(price, 5)))
    
    def print_current_position_value(self, bar):
        ''' 
        Prints out the current position value.
        '''
        date, price, spread = self.get_values(bar)
        cpv = self.units * price
        if self.print_log:
            print("{} |  Current Position Value = {}".format(date, round(cpv, 2)))
    
    def print_current_nav(self, bar):
        ''' 
        Prints out the current net asset value.
        '''
        date, price, spread = self.get_values(bar)
        nav = self.current_balance + self.units * price
        if self.print_log:
            print("{} |  Net Asset Value = {}".format(date, round(nav, 2)))
        
    def go_long(self, bar, units = None, amount = None):
        '''
        Change to long position by buying in units of instrument or amount of money.
        
            Parameters:
                amount (str/int): in numerical value or 'all' to indicate entire balance
        '''
        if self.position == -1:
            self.buy_instrument(bar, units = -self.units) # if short position, go neutral first
        if units:
            self.buy_instrument(bar, units = units)
        elif amount:
            if amount == "all":
                amount = self.current_balance
            self.buy_instrument(bar, amount = amount) # go long

    def go_short(self, bar, units = None, amount = None):
        '''
        Change to short position by selling in units of instrument or amount of money.
        
        Parameters:
                amount (str/int): in numerical value or 'all' to indicate entire balance
        '''
        if self.position == 1:
            self.sell_instrument(bar, units = self.units) # if long position, go neutral first
        if units:
            self.sell_instrument(bar, units = units)
        elif amount:
            if amount == "all":
                amount = self.current_balance
            self.sell_instrument(bar, amount = amount) # go short
        
    def close_pos(self, bar):
        ''' 
        Closes out a long or short position and go neutral.
        '''
        date, price, spread = self.get_values(bar)
        if self.print_log:
            print(75 * "-")
            print("{} | +++ CLOSING FINAL POSITION +++".format(date))
        self.current_balance += self.units * price
        self.current_balance -= (abs(self.units) * spread/2 * self.use_spread) # substract half-spread costs
        if self.print_log:
            print("{} | closing position of {} for {}".format(date, self.units, price))
        self.units = 0 
        self.trades += 1
        perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
        self.print_current_balance(bar)
        if self.print_log:
            print("{} | net performance (%) = {}".format(date, round(perf, 2) ))
            print("{} | number of trades executed = {}".format(date, self.trades))
            print(75 * "-")
        
    def pre_test_cleanup(self, strategy):
        '''
        Reset position, trades, intitial balance and data. 
        Display test title for logging purposes.
        '''
        title = 'Testing {} strategy | {}'.format(strategy, self.symbol)
        if self.print_log:
            print("-" * 75)
            print(title)
            print("-" * 75)
        
        self.position = 0  
        self.trades = 0  
        self.current_balance = self.initial_balance  
        self.process_data() 

