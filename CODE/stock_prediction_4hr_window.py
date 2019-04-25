import glob
import json
import pandas as pd

from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

files = glob.glob('../DATA/A*/A*/*.json')
sentimentAnalyzer = SentimentIntensityAnalyzer()

with open('tweet_sentiment_4hr.csv', 'w+') as sfl:
    for file in files:
        with open(file) as fl:
            lines = fl.readlines()
            tweets = json.loads(lines[0])
            for tweet in tweets:
                # date = time.strftime('%Y/%m/%d', time.localtime(int(tweet['time'])))
                scores = sentimentAnalyzer.polarity_scores(tweet['text'])
                sfl.write(
                    str(tweet['time']) + ',' + str(scores['pos']) + ',' + str(scores['neg']) + ','
                    + str(scores['neu'])
                    + ',' + str(scores['compound']))
                sfl.write('\n')

prices = pd.read_csv('../DATA/CHARTS/APPLE240.csv').values
all_tweets = pd.read_csv('tweet_sentiment_4hr.csv').values

with open('features_4hr.csv', 'w+') as fl:
    for price in prices:
        current_time = (datetime.strptime(price[0] + ' ' + price[1], '%Y.%m.%d %H:%M') - datetime(1970, 1, 1)) \
            .total_seconds()
        epoch_4hr_before = current_time - 14400;
        tweets = all_tweets[(all_tweets[:, 0] >= epoch_4hr_before) & (all_tweets[:, 0] <= current_time)]

        if len(tweets) != 0:
            if float(price[5]) >= float(price[2]):
                label = "1"
            else:
                label = "0"

            for tweet in tweets:
                fl.write(price[0] + ',' + str(tweet[1]) + ',' + str(tweet[2]) + ','
                         + str(tweet[3]) + ',' + str(tweet[4]) + ',' + label)
                fl.write('\n')

dataset = pd.read_csv('features_4hr.csv')
X = dataset.iloc[:, [0, 1, 2, 3]].values
y = dataset.iloc[:, 4].values

scaler = StandardScaler()
X[:, :] = scaler.fit_transform(X[:, :])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

rf = RandomForestClassifier(n_estimators=2000, criterion='entropy')
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print((cm[0, 0] + cm[1, 1])/(cm[0, 0] + cm[1, 1] + cm[1, 0] + cm[0, 1]))

svc = SVC(kernel='rbf', random_state=0)
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print((cm[0, 0] + cm[1, 1])/(cm[0, 0] + cm[1, 1] + cm[1, 0] + cm[0, 1]))

mlp = MLPClassifier(hidden_layer_sizes=(300, 300, 300, 300), random_state=10)
mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print((cm[0, 0] + cm[1, 1]) / (cm[0, 0] + cm[1, 1] + cm[1, 0] + cm[0, 1]))
