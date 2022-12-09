This is a repository of SP500 trading strategies for personal projects and internship.

SP500_Companies.ipynb:
- Scrapes 500 tickers in SP500 index using BeautifulSoup
- Loads OHLC prices for each ticker using yfinance
- Saves ticker OHLC prices into SP500_Companies.csv

SP500_TA.ipynb:
- Calculates technical indicators for each ticker using 5 and 15 days periods
- SMA Ratio
- SMA Volume Ratio
- ATR (Average True Range) Ratio
- ADX (Average Directional Index) Ratio
- RSI (Relative Strength Indicator) Ratio
- MACD (Moving Average Convergence Divergence)
- RC (Rate of Change)
- Saves technical indicator into SP500_TI.csv

Training periods:
- 2011-2015: low rates, steady growth
- 2005-2015: includes Global Financial Crisis recession

Testing periods:
- Period 1 2016-2020: low rates, steady growth, Covid-19 recession
- Period 2 2016-2022: includes record high rates, cost-push inflation, bearish outlook

Objective:
- Beat buy-and-hold strategy
- 17.2% annualised return in period 1
- 13.4% annualised return in period 2

Period 1 strategies performance:
- 2-step KMeans (Euclidean distance) and Gaussian Mixture Clustering with RandomForest classification (28.4% annualised return)
- 2-step KMeans (DTW distance) and Gaussian Mixture Clustering with RandomForest classification (43.8% annualised return)
- Convolutional and Fully-Connected Deep Neural Network (22.2% annualised return)
- KMedoids (DTW distance) Clustering with LSTM (30.0% annualised return)

Period 2 strategies performance:
- 2-step KMeans (Euclidean distance) and Gaussian Mixture Clustering with RandomForest classification (% annualised return)
- 2-step KMeans (DTW distance) and Gaussian Mixture Clustering with RandomForest classification (% annualised return)
- Convolutional and Fully-Connected Deep Neural Network (16.5% annualised return)
- KMedoids (DTW distance) Clustering with LSTM (% annualised return)