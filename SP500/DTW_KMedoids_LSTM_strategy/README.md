# KMedoids Clustering using Dynamic Time Warping (DTW) Distance with LSTM Price Prediction

Modified from: https://link.springer.com/article/10.1007/s11280-021-01003-0

# 1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices using yfinance

# 2. Weekly Strategy:
- Predict the closing price 30 days ahead
- Long if closing price > next day's opening price
- Neutral otherwise
- Close position from 30 days ago

# 3. KMedoid DTW clustering:
- Initialise DTW K-Medoids clustering for 2 to 20 clusters based on log-return
- Determine optimal number of clusters using Elbow Method and Davies-Bouldin Scores
- Apply DTW K-Medoids clustering using determined number of clusters

# 4. Training LSTM Model:
- Predictor variables - normalised current and 99-days lagged normalised closing prices
- Response variable - "Target_Direction" = 1 if Close +30d > Open +1d else 0
- Train dataset: 3/1/2011 to 31/12/2015

# 5. LSTM Architecture:
- Input layer of (100, 1)-dimension
- LSTM layer with 128 neurons, tanh activation
- Output layer of (1,)-dimension, sigmoid activation
- Dropout layer with probability 0.2
- Early stopping if loss does not decrease for 3 epochs

# 6. Making Predictions:
- Use each cluster-specific model to predict probability of Close +30d > Open +1d for each ticker in cluster
- Long the top 20 tickers with highest probabilities

# 7. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|57.5%|
|Gross returns|1.860|1.983|
|Annualised returns|17.2%|19.7%|
|Sharpe ratio|0.376|0.413|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|56.1%|
|Gross returns|1.935|2.084|
|Annualised returns|13.7%|15.9%|
|Sharpe ratio|0.302|0.337|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/DTW_KMedoids_LSTM_strategy/Long-only%20PnL.png)