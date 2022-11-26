KMedoids Clustering using Dynamic Time Warping (DTW) distance with LSTM price prediction

Modified from: https://link.springer.com/article/10.1007/s11280-021-01003-0

1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices from 1/5/2004 to 31/10/2022 using yfinance

2. Data Preprocessing:
- Standardise closing prices for clustering
- Normalise current and 99-days lagged closing prices for prediction

3. Weekly Strategy:
- Predict the closing price 7 days ahead
- Long if closing price > next day's opening price
- Neutral otherwise
- Close position from 7 days ago

4. KMedoid DTW clustering:
- Initialise DTW K-Medoids clustering for 2 to 50 clusters based on log-return from standardised closing prices
- Determine optimal number of clusters using Elbow Method and Davies-Bouldin Scores
- Apply DTW K-Medoids clustering using determined number of clusters

5. Training LSTM Model:
Predictor variables - current and 99-days lagged normalised closing prices
- Response variable - (Close +7d - Open +1d)/Close +7d
- Train dataset: 3/1/2005 to 31/12/2014
- Validation dataset: 1/1/2015 to 31/12/2015
- Set early stopping if Mean Absolute Error does not decrease after 3 epochs
= Combine train and validation datasets and refit model until stopped epoch

6. LSTM Architecture:
- Input layer of (100, 1)-dimension
- Lambda layer
- LSTM layer with 128 neurons, ReLu activation
- Output layer of (1,)-dimension, linear activation
- Adam  optimizer

7. Making Predictions:
- Test dataset: 4/1/2016 to 31/12/2020
- Predict "Target"

8. Performance:
- Mean MAE across tickers: 0.0341
- Mean RMSE across tickers: 0.0491
- Buy-and-Hold gross returns = 1.860
- Strategy gross returns = 2.502
- Buy-and-Hold Sharpe ratio = 0.167
- Strategy Sharpe ratio = 0.175