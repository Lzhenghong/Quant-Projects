# 2-Step KMeans and Gaussian Mixture Clustering with RandomForest Classification using Euclidean Distance

Modified from: https://towardsdatascience.com/implementation-of-technical-indicators-into-a-machine-learning-framework-for-quantitative-trading-44a05be8e06

# 1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices using yfinance 

# 2. Data Preprocessing:
- Calculated the following technical indicators for each ticker using 5 and 15 days period
- SMA Ratio
- SMA Volume Ratio
- ATR (Average True Range) Ratio
- ADX (Average Directional Index) Ratio
- RSI (Relative Strength Indicator) Ratio
- MACD (Moving Average Convergence Divergence)
- RC (Rate of Change)

# 3. Weekly Strategy:
- Predict the closing price 7 days ahead
- Long if closing price > next day's opening price
- Neutral otherwise
- Close position from 7 days ago

# 4. 2-Step Clustering using KMeans and Gaussian Mixture:
- Feature engineer an "aggregate" variable by multiplying all the technical indicators together and with log-return
- Apply MinMaxScaler to "aggregate" variable
- Initialise clustering using KMeans for 1 to 50 clusters based on "aggregate" across time
- Determine optimal number of clusters using Elbow Method and Silhouette Scores
- Apply Gaussian Mixture clustering
- For each level-1 cluster, repeat the clustering based on OneHotEncoded "industry" variable for 1 to 10 clusters
- Feature engineer weekly lagged values for each technical indicators and log-return

# 5. Training RandomForestClassifier Model:
- Predictor variables - current and 6-days lagged technical indicators + log-return
- Response variable - "Target_Direction" = 1 if Close +7d > Open +1d
- Train dataset: 3/1/2011 to 31/12/2015
- For each level-2 cluster, fit model using GridSearch Cross Validation

# 6. Making Predictions:
- Use each cluster-specific model to predict probability of Close +7d > Open +1d for each ticker in cluster
- Long the top 20 tickers with highest probabilities

# 7. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|56.1%|
|Gross returns|1.860|2.672|
|Annualised returns|17.2%|33.4%|
|Sharpe ratio|0.167|0.207|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|55.4%|
|Gross returns|1.935|2.909|
|Annualised returns|13.4%|27.3%|
|Sharpe ratio|0.134|0.168|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/KMeans_GMM_RF_strategy/Long-only%20PnL.png)
