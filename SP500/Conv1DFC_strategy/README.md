# Convolutional1D and Fully-Connected Deep Neural Network

Modified from: https://arxiv.org/pdf/2103.14080.pdf

# 1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices using yfinance 

# 2. Data Preprocessing:
- Scale volume down to same magnitude as closing price

# 3. Strategy:
- Predict the closing price 7 days ahead
- Long for next 7 days if closing price > next day's opening price
- Short for next 7 days if closing price > 2% lower than next day's opening price
- Neutral otherwise
- Close position after 7 days if any

# 4. Training DNN Model:
- Predictor variables - current and 13-days lagged closing prices + volume
- Response variable - "Target_Direction" = 1 if long, 0 if neutral, -1 if short
- Train dataset: 3/1/2011 to 31/12/2014
- Validation dataset: 2/1/2015 to 31/12/2015
- Fit data in batches of size 32
- Set early stopping if validation loss does not decrease after 10 epochs
- Combine train and validation datasets and refit the model until stopped epoch

# 5. DNN Architecture:
- Input layer of (14,2)-dimension
- Conv1D layer with 4 filters of size 3, ReLu activation
- Flatten layer
- Dense layer with 128 neurons, ReLu activation
- Output layer of (1,)-dimension, sigmoid activation
- RMSprop optimizer

# 6. Making Predictions:
- Predict "Target_Direction" and use as signal for next 7 days

# 7. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|61.0%|
|Gross returns|1.860|2.111|
|Annualised returns|17.2%|22.2%|
|Sharpe ratio|0.167|0.223|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|59.5%|
|Gross returns|1.935|2.154|
|Annualised returns|13.7%|16.9%|
|Sharpe ratio|0.134|0.166|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/Conv1DFC_strategy/Long-short%20PnL.png)