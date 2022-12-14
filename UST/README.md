# US Treasuries Trading Strategies

# 1. Training Periods:
- 2005-2015: US Housing Boom, Global Financial Crisis (GFC), post-GFC recovery

# 2. Testing Periods:
- Period 1 2016-2020: decade-long bull market, Powell Pirouette, 2020 Covid-19 recession
- Period 2 2016-2022: includes post-Ukraine invasion stagflation, record Fed hike

# 3. Macroeconomic Regimes

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/UST/US%20EFFR%20chart.png)

# 4. Objective:
- Beat buy-and-hold strategy of iShares US Treasury Bond ETF in gross returns and/or Sharpe ratio

# 5. Strategies:
- Regime-Specific RandomForest Classification for Mark-to-Market Return Prediction
- Regime-Specific RandomForest Classification for Yield Curve Level Mean Reversion

# 6. Performance Summary:

|Period 1|iShares ETF|Yield-Momentum|Level Mean Reversion|Slope Mean Reversion|
|---|---|---|---|---|
|Gross returns|1.084|0.792|0.8527|0.8526|
|Annualised returns|1.68%|-4.16%|-2.95%|-2.95%|
|Sharpe ratio|0.113|-0.153|-0.145|-0.145|

|Period 2|iShares ETF|Yield-Momentum|Level Mean Reversion|Slope Mean Reversion|
|---|---|---|---|---|
|Gross returns|0.924|1.031|1.080|1.083|
|Annualised returns|-1.09%|0.443%|1.14%|1.19%|
|Sharpe ratio|0.102|0.033|0.064|0.065|