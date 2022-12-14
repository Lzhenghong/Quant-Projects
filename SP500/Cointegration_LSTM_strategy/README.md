# Cointegrated Pairs Trading with LSTM

Modified from: https://towardsdatascience.com/implementation-of-technical-indicators-into-a-machine-learning-framework-for-quantitative-trading-44a05be8e06

# 1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Scraped top 50 companies based on market capitalisation using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices using yfinance

# 2. Weekly Strategy:
- For each cointegrated pair, predict the spread 7 days ahead
- Calculate the difference between current and predicted spread
- Short if difference > 0.5 * 30-days SMA of standard deviation of positive difference
- Long if difference < -0.5 * 30-days SMA of standard deviation of negative difference
- Neutral otherwise

# 3. Cointegration Test:
- Conduct Engle-Granger cointegration test on top 50 companies
- Obtain top 10 cointegrated pairs based on p-values

# 4. Training LSTM Model:
- Fit an LSTM model for each cointegrated pair
- Predictor variables - current and 99-days lagged spread difference
- Response variable - "signal" = 1 if long, 0 if neutral, -1 if short
- Train dataset: 3/1/2011 to 31/12/2014
- Validation dataset: 1/1/2015 to 31/12/2015
- Set early stopping if validation loss does not decrease after 3 epochs
- Combine train and validation datasets and refit model until stopped epoch

# 6. LSTM Architecture:
- Input layer of (100,)-dimension
- Lambda layer to transform output to (1, 100, 1)-dimension
- LSTM layer with 128 neurons, ReLu activation
- Output layer of (1,)-dimension, linear activation
- Adam  optimizer

# 7. Making Predictions:
- For each pair, predict the "signal" variable and rebalance the portfolio every 7 days

# 8. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|40.9%|
|Gross returns|1.860|1.521|
|Annualised returns|17.2%|10.4%|
|Sharpe ratio|0.167|0.160|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|40.2%|
|Gross returns|1.935|1.680|
|Annualised returns|13.7%|9.96%|
|Sharpe ratio|0.134|0.145|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/Cointegration_LSTM_strategy/spread%20trading%20PnL.png)
