import sys
import pandas
import numpy as np
from sklearn import tree

columns = [
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

df = pandas.read_csv('data/cleaned.csv')
data1 = df[(df['category'] == 'Actor') & (df['year'] < 2016)][columns]
# data2 = df[(df['category'] == sys.argv[0]) & (df['year'] == 2016)][['name'] + columns]

accuracy = []

data = data1.values.tolist()
train_cutoff = int(len(data) * 0.60)

for i in range(0, 501):
    np.random.shuffle(data)

    X = [ i[1:] for i in data ]
    Y = [ i[0]  for i in data ]

    X_train = X[:train_cutoff]
    Y_train = Y[:train_cutoff]
    X_test = X[train_cutoff:]
    Y_test = Y[train_cutoff:]

    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(X_train, Y_train)

    Y_predict = classifier.predict(X_test)

    equal = 0
    for i in xrange(len(Y_predict)):
        if Y_predict[i] == Y_test[i]:
            equal += 1

    accuracy.append((float(equal)/len(Y_predict)))

print round(sum(accuracy) / len(accuracy), 4) * 100
