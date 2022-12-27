# SP500 Trading Strategies

# 1. Training periods:
- 2011-2015: low rates, post Global Financial Crisis recovery
- 2005-2015: includes 2008 Global Financial Crisis and 2010 Eurozone Crisis

# 2. Testing periods:
- Period 1 2016-2020: gradual rates rise, steady growth, 2018 Crypto crash and 2020 Covid-19 recession
- Period 2 2016-2022: includes record high rates, post Ukraine invasion stagflation

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/SP500%20macro%20chart.png)

# 3. Objective:
- Beat buy-and-hold strategy in gross returns and/or Sharpe ratio

# 4. Strategies:
- 2-Step KMeans (Euclidean Distance) and Gaussian Mixture Clustering with RandomForest Classification for Signal Prediction
- 2-Step KMeans (DTW Distance) and Gaussian Mixture Clustering with RandomForest Classification for Signal Prediction
- Convolutional and Fully-Connected Deep Neural Network for Signal Prediction
- KMedoids (DTW Distance) Clustering with LSTM for Price Prediction
- Cointegrated Pairs Trading with LSTM for Signal Prediction

# 5. Performance Summary:

|Period 1|Buy-and-hold|KMeans-GMM-RF (Euclidean)|KMeans-GMM-RF (DTW)|Conv1DFC|KMedoids-LSTM|Cointegration-LSTM|
|---|---|---|---|---|---|---|
|Gross returns|1.860|2.672|2.616|2.111|2.412|4.230|
|Annualised returns|17.2%|33.4%|32.3%|22.2%|28.2%|64.6%|
|Sharpe ratio|0.167|0.207|0.208|0.223|0.129|1.198|

|Period 2|Buy-and-hold|KMeans-GMM-RF (Euclidean)|KMeans-GMM-RF (DTW)|Conv1DFC|KMedoids-LSTM|Cointegration-LSTM|
|---|---|---|---|---|---|---|
|Gross returns|1.935|2.909|2.994|2.154|2.678|8.491|
|Annualised returns|13.7%|28.0%|29.2%|16.9%|24.6%|109.7%|
|Sharpe ratio|0.134 (7D)/0.302 (30D)|0.168|0.175|0.166|0.114|1.224|