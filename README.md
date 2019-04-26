# Directional-Stock-Prediction
CSE 573 Group Project

The repository contains 3 main folders:

CODE - Contains all the code files -  
  1. Contains data scraper code 
  2. Contains directional model code for 1day window
  3. Contains directional model code for 4hr window

  To run the above code, just run like any other python file ------ python <file_name.py>

DATA - Contains all the data for the model. Please unzip AAPL.zip and AMZN.zip, contains all the tweets from [2014-2019]

EVALUATIONS - Contains images showing graphs of models results.

------------------------------------------------------------------------------------------------------------------------------
DIRECTIONAL MODEL:

We have built 2 models depending on window size.
1.  1-Day window
2.  4-Hr Window

For 1-day window model, we take tweets of the previous day, compute the sentiment scores using VADER algorithm and then use the output of VADER as features for our model. We use the same strategy for 4hr window model.

Feature Matrix:
Independent Variables: [pos_score,neg_score,neu_score,compund_score]
Dependent Variables: Class Label [1/0]

We use the historical data which contains daily and 4hr prices. We label the data accordingly; 
if close_price >= open_price
  label = 1
else 
  label = 0

We have built three models:
1.  Random Forest
2.  SVM
3.  MLP

Results: 
  After cross validation, we achieved an accuracy of around ~73%
  
------------------------------------------------------------------------------------------------------------------------------

SCRAPER:

We have two kinds of scrapers which face to two different sources, Nasdaq website and StockTwits. For the Nasdaq news scraper, you can specify the stock symbol and the most recent date, and the scraper will scrap foward to the past until there is no news. For the StockTwits scraper, you use the tweet ID of the most recent tweets and the stock symbol that you want to scrape. And the scraper will use RESTful API to fetch older tweets until the date that you specified.

------------------------------------------------------------------------------------------------------------------------------
RUN INSTRUCTIONS:

1. python3 and pip need to be present in the system.

2. Use our starter_prg.py (Under Code folder) to install required libraries(like sklearn, vader sentiment, etc) and run our      model.
            python starter_prg.py
3. Accuracy results will be displayed in the console.
------------------------------------------------------------------------------------------------------------------------------
    
