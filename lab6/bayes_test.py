import csv
import string
from bayes import NaiveBayesClassifier


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    with open('data/SMSSpamCollection') as f:
        data = list(csv.reader(f, delimiter="\t"))
    titles, labels = [], []
    for tagged_message in data:
        labels.append(tagged_message[0])
        titles.append(tagged_message[1])
    titles = [clean(title).lower() for title in titles]
    titles_training, labels_training, titles_test, labels_test = titles[0:3900], labels[0:3900], titles[3900:], labels[3900:]
    
    model = NaiveBayesClassifier()
    model.fit(titles_training, labels_training)
    model.predict(titles_test)
    print(model.score(titles_test, labels_test), "%")
