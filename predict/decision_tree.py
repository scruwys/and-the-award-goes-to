"""
This predicts Oscar wins using a Decision Tree classifier.
"""
import util
import argparse
import numpy as np
from sklearn import tree

parser = argparse.ArgumentParser()
parser.add_argument('--award')
parser.add_argument('--year')
args = parser.parse_args()

if __name__ == '__main__':
    past, future = util.load_data(args.award, 1990, int(args.year))
    train_cutoff = int(len(past) * 0.60)

    accuracy = []

    films_CY = [ i[0] for i in future ]
    feats_CY = [ i[2:] for i in future ]

    guesses = {}

    for film in films_CY:
      guesses[film] = 0.0

    for _ in range(0, 501):

        np.random.shuffle(past)

        X = [ i[1:] for i in past ]
        Y = [ i[0]  for i in past ]

        X_train = X[:train_cutoff]
        Y_train = Y[:train_cutoff]
        X_test  = X[train_cutoff:]
        Y_test  = Y[train_cutoff:]

        classifier = tree.DecisionTreeClassifier()
        classifier = classifier.fit(X_train, Y_train)

        for idx, film in enumerate(films_CY):      
          guesses[film] += float(classifier.predict([feats_CY[idx]])[0])

    util.print_predictions_for(guesses, "Decision Trees - Predictions for {0}:".format(args.award))
    
    # Declare the highest percentage the winner.
    print "\nAnd the award goes to... {0} !!!".format(max(guesses, key=guesses.get))