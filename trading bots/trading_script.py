from TechnicalTraders import *

if __name__ == "__main__":
        
    trader = SMATrader("oanda.cfg", "EUR_USD", "1min", 1000, "17:00", SMA_S = 50, SMA_L = 200)
    trader.get_most_recent()
    # trader.stream_data(trader.instrument)
    trader.stream_data(trader.instrument, stop=100)
    if trader.position != 0: 
        close_order = trader.create_order(trader.instrument, units = -trader.position * trader.units, 
                                          suppress = True, ret = True) 
        trader.report_trade(close_order, "GOING NEUTRAL")
        trader.position = 0

