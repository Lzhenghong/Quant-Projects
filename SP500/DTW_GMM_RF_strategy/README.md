2-step KMeans and Gaussian Mixture Clustering with RandomForest classification using Dynamic Time Warping (DTW) distance

Modified from: https://towardsdatascience.com/implementation-of-technical-indicators-into-a-machine-learning-framework-for-quantitative-trading-44a05be8e06

1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices from 1/1/2011 to 31/12/2020 using yfinance 

2. Data Preprocessing:
- Calculated the following technical indicators for each ticker using 5 and 15 days period
- SMA Ratio
- SMA Volume Ratio
- ATR (Average True Range) Ratio
- ADX (Average Directional Index) Ratio
- RSI (Relative Strength Indicator) Ratio
- MACD (Moving Average Convergence Divergence)
- RC (Rate of Change)

3. Weekly Strategy:
- Predict the closing price 7 days ahead
- Long if closing price > next day's opening price
- Neutral otherwise
- Close position from 7 days ago

4. 2-Step Clustering using KMeans and Gaussian Mixture:
- Winsorise top and bottom 10% of each technical indicators
- Initialise DTW K-Means clustering for 1 to 50 clusters based on log-return across time
- Determine optimal number of clusters using Elbow Method and Silhouette Scores
- Apply DTW K-Means clustering using determined number of clusters
- For each level-1 cluster, repeat the clustering based on OneHotEncoded "industry" variable for 1 to 10 clusters
- Feature engineer weekly lagged values for each technical indicators and log-return

5. Training RandomForestClassifier Model:
- Predictor variables - current and 6-days lagged technical indicators + log-return
- Response variable - "Target_Direction" = 1 if Close +7d > Open +1d
- Train dataset: 3/1/2011 to 31/12/2015
- Test dataset: 4/1/2016 to 30/12/2020
- Plot validation curve to estimate parameter ranges
- For each level-2 cluster, fit model using GridSearch Cross Validation

6. Making Predictions:
- Use each cluster-specific model to predict probability of Close +7d > Open +1d for each ticker in cluster
- Long the top 20 tickers with highest probabilities

7. Performance:
- 91.3% train accuracy
- 56.1% test accuracy
- Buy-and-Hold gross returns = 1.860
- Strategy gross returns = 3.192
- Buy-and-Hold Sharpe ratio = 41.2
- Strategy Sharpe ratio = 29.4