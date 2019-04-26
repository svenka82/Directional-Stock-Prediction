# Directional-Stock-Prediction
CSE 573 Group Project

The repository contains 3 main folders:

1. CODE - Contains all the code files.
  a. Contains data scraper code 
  b. Contains directional model code for 1day window
  c. Contains directional model code for 4hr window

  To run the above code, just run like any other python file. 
    python <file_name.py>

2. DATA - Contains all the data for the model.
  Please unzip AAPL.zip and AMZN.zip - contains all the tweets from 2014-2019

3. EVALUATIONS - Contains images showing graphs of models results.

------------------------------------------------------------------------------------------------------------------------------
DIRECTIONAL MODEL:

We have built 2 models depending on window size.
1.  1-Day window
2.  4-Hr Window

For 1-day window model, we take tweets of the previous day, compute the sentiment scores using VADER algorithm and then use the output of VADER as features for our model.

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
