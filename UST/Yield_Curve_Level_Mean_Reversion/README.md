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
- Obtain reference average spot curve during QE from 2007-08-17 to 2015-12-15
- Obtain reference average spot curve during QT from 2005-01-04 to 2007-08-16

# 3. Monthly Strategy:
- Predict spread between current mean level of spot curve and reference spot curve for 1M, 10Y and 20Y spot rates
- Long UST bonds if spread > 0, else short
- Equal weights for each UST debt
- Close position from 30 days ago

# 4. Yield Curve Factors:
- 5-year, 7-year, 10-year and 20-year real par rates
- Spot curve level spread from reference spot curve

# 5. Momentum Factors
- "Inverse wealth" = 1 if current S&P 500 index > past 180-days weighted average 
- "Momentum" = 1 if current 20-years spot rate > past 180-days weighted average by more than 5 bps, - 1 if < past weighted average by more than 5 bps
- Effective Fed Fund rates

# 6. Regime Switching
- "Fed regime" = 0 for periods of QE, 1 for periods of QT, 2 for periods of constant low rates
- periods of QE - 2007-2009 GFC, 2019 Powell Pirouette, 2020 Covid recession
- Periods of QT - 2005-2007 US Housing Boom, 2016-2019 bull market, 2022 post-Ukraine Fed hike
- periods of constant low rates - 2009-2015 post-GFC recovery

# 7. Training RandomForestClassifier Model:
- Predictor variables - current and 99-days lagged yield curve, momentum and value factors
- Response variable - "signal" = 1 if spread > 0 else -1 for 1M, 10Y and 20Y UST bonds
- Train dataset: 1/7/2005 to 31/12/2015
- For each regime and 3 UST bonds, conduct hyperparameter tuning using validation curve
- Fit model for each regime using GridSearchCV

# 8. Making Predictions:
- Use each regime-specific model to predict probability of spot curve moving up or down 30 days later for each UST bond
- Long if more likely to move down, short otherwise

# 9. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Mean Hit rate|-|93.7%|
|Gross returns|1.084|0.8527|
|Annualised returns|1.68%|-2.95%|
|Sharpe ratio|0.113|-0.145|

|Jan 2016 - Dec 2022|Buy-and-hold|Strategy|
|---|---|---|
|Mean Hit rate|-|94.3%|
|Gross returns|0.924|1.080|
|Annualised returns|-1.09%|1.14%|
|Sharpe ratio|-0.102|0.064|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/UST/Yield_Curve_Level_Mean_Reversion/level%20mean%20reversion%20pnl.png)

# 10. Prediction Analysis

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/UST/Yield_Curve_Level_Mean_Reversion/prediction%20breakdown.png)


