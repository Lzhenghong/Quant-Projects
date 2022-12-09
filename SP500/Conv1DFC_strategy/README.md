Convolutional1D and Fully-Connected Deep Neural Network

Modified from: https://arxiv.org/pdf/2103.14080.pdf

1. Data Collection:
- Scraped ticker data for each company in SP500 using BeautifulSoup
- Loaded SPY and each SP500 ticker OHLC prices from 1/1/2011 to 28/10/2022 using yfinance 

2. Data Preprocessing:
- Scale volume down to same magnitude as closing price
- Period 1 back-testing: 4/1/2016 to 31/12/2020
- Period 2 back-testing: 4/1/2016 to 28/10/2022

3. Strategy:
- Predict the closing price 7 days ahead
- Long for next 7 days if closing price > next day's opening price
- Short for next 7 days if closing price > 2% lower than next day's opening price
- Neutral otherwise
- Close position after 7 days if any

4. Training DNN Model:
- Predictor variables - current and 13-days lagged closing prices + volume
- Response variable - "Target_Direction" = 1 if long, 0 if neutral, -1 if short
- Train dataset: 3/1/2011 to 31/12/2014
- Validation dataset: 2/1/2015 to 31/12/2015
- Fit data in batches of size 32
- Set early stopping if validation loss does not decrease after 10 epochs
- Combine train and validation datasets and refit the model until stopped epoch

5. DNN Architecture:
- Input layer of (14,2)-dimension
- Conv1D layer with 4 filters of size 3, ReLu activation
- Flatten layer
- Dense layer with 128 neurons, ReLu activation
- Output layer of (1,)-dimension, sigmoid activation
- RMSprop optimizer

6. Making Predictions:
- Test dataset (period 1): 4/1/2016 to 31/12/2020
- Test dataset (period 2): 4/1/2016 to 28/10/2022
- Predict "Target_Direction"

7. Performance (period 1):
- 61.0% test accuracy
- Buy-and-Hold gross returns = 1.860
- Strategy gross returns = 2.111
- Buy-and-Hold Sharpe ratio = 0.167
- Strategy Sharpe ratio = 0.223

8. Performance (period 2):
- 59.5% test accuracy
- Buy-and-Hold gross returns = 1.935
- Strategy gross returns = 2.154
- Buy-and-Hold Sharpe ratio = 0.134
- Strategy Sharpe ratio = 0.166