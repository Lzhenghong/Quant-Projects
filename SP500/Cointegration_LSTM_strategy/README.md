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
- Indicators - spread, 30-days spread difference, spread SMA ratio, spread RSI ratio, spread MACD
- Fit an LSTM model for each cointegrated pair
- Predictor variables - current and 30-days lagged indicators
- Response variable - "signal" = 1 if long, 0 if neutral, -1 if short
- Train dataset: 3/1/2011 to 31/12/2015
- Train for 15 epochs for each pair

# 6. LSTM Architecture:
- Input layer of (30, 5)-dimension
- LSTM layer with 128 neurons, ReLu activation
- Output layer of (3,)-dimension, linear activation
- Adam  optimizer

# 7. Making Predictions:
- For each pair, predict the "signal" variable and rebalance the portfolio every 30 days

# 8. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|87.9%|
|Gross returns|1.860|4.230|
|Annualised returns|17.2%|64.6%|
|Sharpe ratio|0.376|1.198|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|87.7%|
|Gross returns|1.935|8.491|
|Annualised returns|13.7%|109.7%|
|Sharpe ratio|0.302|1.224|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/Cointegration_LSTM_strategy/spread%20trading%20PnL.png)
