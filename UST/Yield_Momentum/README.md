# Regime-Specific RandomForest Classification for Mark-to-Market Return Prediction

Modified from: https://www.aqr.com/Insights/Research/Journal-Article/Forecasting-US-Bond-Returns

# 1. Data Collection:
- Downloaded US Treasury par (real) yield curve rates from US Department of Treasury
- Extracted 1-month and 3-months Treasury bill yield-to-maturities from Bloomberg
- Downloaded US Effective Fed Fund Rates from https://fred.stlouisfed.org/series/DFF

# 2. Data Preprocessing:
- Interpolate daily par yield curve rates for 1.5 to 19.5 years using Cubic Hermite Spline
- Bootstrap daily spot rates for 6 months to 20 years
- Interpolate daily 1-month and 3-months US Treasury Bill spot rates using Cubic Spline

# 3. Monthly Strategy:
- Predict the 20-year UST bond's spot rate 30 days ahead
- Long if spot rate > next day's spot rate
- Short otherwise
- Holding weight in portfolio is determined by predicted probability
- Remaining weight is allocated to holding 1-month UST bill
- Close position from 30 days ago

# 4. Yield Curve Factors:
- Implied 1-month to 20-years spot rates
- 5-year, 7-year, 10-year and 20-year real par rates

# 5. Momentum Factors
- "Inverse wealth" = 1 if current S&P 500 index > past 180-days weighted average 
- "Momentum" = 1 if current 20-years spot rate > past 180-days weighted average by more than 5 bps, - 1 if < past weighted average by more than 5 bps
- Effective Fed Fund rates

# 6. Regime Switching
- "Fed regime" = 0 for periods of QE, 1 for periods of QT
- periods of QE - 2007-2015 GFC and post-GFC, 2019 Powell Pirouette, 2020 Covid recession
- Periods of QT - 2005-2007 US Housing Boom, 2016-2019 bull market, 2022 post-Ukraine Fed hike

# 7. Training RandomForestClassifier Model:
- Predictor variables - current and 99-days lagged yield curve, momentum and value factors
- Response variable - "signal" = 1 if 20Y spot rate +30d < 20Y spot rate +1d
- Train dataset: 1/7/2005 to 31/12/2015
- For each regime, conduct hyperparameter tuning using validation curve
- Fit model for each regime using GridSearchCV

# 8. Making Predictions:
- Use each regime-specific model to predict probability of 20Y spot rate +30d > 20Y spot rate +1d for each ticker in cluster
- Long or short 20Y UST bond with portfolio weight = predicted probability
- Remaining portfolio weight is Long 1M UST bill

# 9. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|50.0%|
|Gross returns|1.084|0.792|
|Annualised returns|1.68%|-4.16%|
|Sharpe ratio|0.113|-0.153|

|Jan 2016 - Dec 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|53.4%|
|Gross returns|0.924|1.031|
|Annualised returns|-1.09%|0.443%|
|Sharpe ratio|-0.102|0.033|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/UST/Yield_Momentum/QE%20QT%20PnL.png)
