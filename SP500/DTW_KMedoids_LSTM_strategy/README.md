# KMedoids Clustering using Dynamic Time Warping (DTW) Distance with LSTM Price Prediction

Modified from: https://link.springer.com/article/10.1007/s11280-021-01003-0

# 1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices using yfinance

# 2. Data Preprocessing:
- Standardise closing prices for clustering
- Normalise current and 99-days lagged closing prices for prediction

# 3. Weekly Strategy:
- Predict the closing price 7 days ahead
- Long if closing price > next day's opening price
- Neutral otherwise
- Close position from 7 days ago

# 4. KMedoid DTW clustering:
- Initialise DTW K-Medoids clustering for 2 to 50 clusters based on log-return from standardised closing prices
- Determine optimal number of clusters using Elbow Method and Davies-Bouldin Scores
- Apply DTW K-Medoids clustering using determined number of clusters

# 5. Training LSTM Model:
Predictor variables - current and 99-days lagged normalised closing prices
- Response variable - (Close +7d - Open +1d)/Close +7d
- Train dataset: 3/1/2005 to 31/12/2014
- Validation dataset: 1/1/2015 to 31/12/2015
- Set early stopping if Mean Absolute Error does not decrease after 3 epochs
= Combine train and validation datasets and refit model until stopped epoch

# 6. LSTM Architecture:
- Input layer of (100,)-dimension
- Lambda layer to transform output to (1, 100, 1)-dimension
- LSTM layer with 128 neurons, ReLu activation
- Output layer of (1,)-dimension, linear activation
- Adam  optimizer

# 7. Making Predictions:
- Use each cluster-specific model to predict probability of Close +7d > Open +1d for each ticker in cluster
- Long the top 20 tickers with highest probabilities

# 8. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|MAE|-|0.0338|
|RMSE|-|0.0489|
|Gross returns|1.860|2.412|
|Annualised returns|17.2%|28.2%|
|Sharpe ratio|0.167|0.129|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|MAE|-|0.0349|
|RMSE|-|0.0490|
|Gross returns|1.935|2.678|
|Annualised returns|13.7%|24.6%|
|Sharpe ratio|0.134|0.114|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/DTW_KMedoids_LSTM_strategy/Long-only%20PnL.png)