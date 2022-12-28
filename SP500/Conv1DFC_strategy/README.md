# Convolutional1D and Fully-Connected Deep Neural Network

Modified from: https://arxiv.org/pdf/2103.14080.pdf

# 1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices using yfinance 

# 2. Strategy:
- Predict the closing price 30 days ahead
- Long for next 30 days if closing price > next day's opening price
- Short for next 30 days if closing price > 2% lower than next day's opening price
- Neutral otherwise
- Close position after 30 days if any

# 3. Training DNN Model:
- Predictor variables - normalised current and 99-days lagged closing prices + volume
- Response variable - "Target_direction" = 1 if long, 0 if neutral, -1 if short
- Train dataset: 3/1/2011 to 31/12/2015
- Fit data in batches of size 32
- Set early stopping if loss does not decrease after 2 epochs

# 4. DNN Architecture:
- Input layer of (100,2)-dimension
- Conv1D layer with 4 filters of size 3, ReLu activation
- Flatten layer
- Dense layer with 128 neurons, ReLu activation
- Output layer of (1,)-dimension, softmax activation
- RMSprop optimizer

# 6. Making Predictions:
- Predict "Target_Direction" and use as signal for next 30 days

# 7. Performance:

|Jan 2016 - Dec 2020|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|61.9%|
|Gross returns|1.860|1.836|
|Annualised returns|17.2%|16.7%|
|Sharpe ratio|0.376|0.425|

|Jan 2016 - Oct 2022|Buy-and-hold|Strategy|
|---|---|---|
|Hit rate|-|58.6%|
|Gross returns|1.935|2.109|
|Annualised returns|13.7%|16.2%|
|Sharpe ratio|0.302|0.378|

![alt text](https://github.com/Lzhenghong/Quant-Projects/blob/main/SP500/Conv1DFC_strategy/Long-short%20PnL.png)