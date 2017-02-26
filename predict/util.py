import numpy as np
import pandas as pd

relevant_columns = [
  'Oscar',
  'BAFTA',
  'Golden Globe',
  'Guild',
  'q1_release',
  'q2_release',
  'q3_release',
  'q4_release',
  'running_time',
  'G',
  'PG',
  'PG13',
  'R',
  'produced_USA',
  'imdb_score',
  'rt_audience_score',
  'rt_critic_score',
  'stars_count',
  'writers_count',
  'box_office'
]


def load_data(award, min_year, prediction_year):
    df = pd.read_csv('data/prepared.csv')
    
    past = df[(df['category'] == award) & (df['year'] < prediction_year) & (df['year'] > min_year)][relevant_columns]
    curr = df[(df['category'] == award) & (df['year'] == prediction_year)][['name']+relevant_columns]

    return past.values.tolist(), curr.values.tolist()


def accuracy(Y_predict, Y_test):
    equal = 0
    for i in xrange(len(Y_predict)):
        if Y_predict[i] == Y_test[i]:
            equal += 1

    return float(equal)/len(Y_predict)


def print_predictions_for(guesses, title):
    total = sum([v for k, v in guesses.items()])

    print
    print title
    print "--------------------------------------------------" 
    for key, value in sorted(guesses.items(), key=lambda x: x[1], reverse=True):
        print round(value / total, 4), "\t", key


def test_for_accuracy(data, classifier, iterations = 200):
    cache = []
    train_cutoff = int(len(data) * 0.60)

    for i in range(0, iterations + 1):
        np.random.shuffle(data)

        X = [ i[1:] for i in data ]
        Y = [ i[0]  for i in data ]

        X_train = X[:train_cutoff]
        Y_train = Y[:train_cutoff]
        X_test  = X[train_cutoff:]
        Y_test  = Y[train_cutoff:]

        classifier = classifier.fit(X_train, Y_train)

        Y_predict = classifier.predict(X_test)
        cache.append(accuracy(Y_predict, Y_test))

    return round(sum(cache) / len(cache), 4) * 100