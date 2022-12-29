# US Treasuries Trading Strategies

# 1. Training periods:
- 2005-2015: US Housing Boom, Global Financial Crisis (GFC), post-GFC recovery

# 2. Testing periods:
- Period 1 2016-2020: decade-long bull market, Powell Pirouette, 2020 Covid-19 recession
- Period 2 2016-2022: includes post-Ukraine invasion stagflation, record Fed hike

# 3. Macroeconomic Regimes

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/UST/US%20EFFR%20chart.png)

# 4. Objective:
- Beat buy-and-hold strategy of iShares US Treasury Bond ETF in gross returns and/or Sharpe ratio

# 5. Strategies:
- Regime-Specific RandomForest Classification for Mark-to-Market Return Prediction

# 6. Performance Summary:

|Period 1|iShares ETF|Yield-Momentum|Level Mean Reversion|
|---|---|---|---|
|Gross returns|1.084|0.792|1.070|
|Annualised returns|1.68%|-4.16%|1.40%|
|Sharpe ratio|0.113|-0.153|0.155|

|Period 2|iShares ETF|Yield-Momentum|
|---|---|---|---|
|Gross returns|0.924|1.031|1.221|
|Annualised returns|-1.09%|0.443%|3.16%|
|Sharpe ratio|0.102|0.033|0.309|