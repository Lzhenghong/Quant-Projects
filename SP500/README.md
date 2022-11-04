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

Strategies:
- 2-step KMeans (Euclidean distance) and Gaussian Mixture Clustering with RandomForest classification
- 2-step KMeans (DTW distance) and Gaussian Mixture Clustering with RandomForest classification