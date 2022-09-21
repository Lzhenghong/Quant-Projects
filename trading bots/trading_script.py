from TechnicalTraders import *

if __name__ == "__main__":
        
    trader = ConTrader("oanda.cfg", "EUR_USD", "1min", window = 1, units = 1000, stop = "17:00")
    trader.get_most_recent()
    # trader.stream_data(trader.instrument)
    trader.stream_data(trader.instrument, stop=100)
    if trader.position != 0: 
        close_order = trader.create_order(trader.instrument, units = -trader.position * trader.units, 
                                          suppress = True, ret = True) 
        trader.report_trade(close_order, "GOING NEUTRAL")
        trader.position = 0

