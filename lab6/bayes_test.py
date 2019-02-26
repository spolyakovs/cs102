import csv
import string
from bayes import NaiveBayesClassifier


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    with open('data/SMSSpamCollection') as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, Y = [], []
    for tagged_message in data:
        Y.append(tagged_message[0])
        X.append(tagged_message[1])
    X = [clean(x).lower() for x in X]
    X_training, Y_training, X_test, Y_test = X[0:3900], Y[0:3900], X[3900:], Y[3900:]
    
    model = NaiveBayesClassifier()
    model.fit(X_training, Y_training)
    model.predict(X_test)
    print(model.score(X_test, Y_test), "%")
