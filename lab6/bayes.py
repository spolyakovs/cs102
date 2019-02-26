from math import log


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.words_list = []
        self.words_prob = {}
        self.tags_list = []
        self.tags_prob = {}

    def fit(self, X, Y):
        """ Fit Naive Bayes classifier according to X, Y. """
        if len(X) != len(Y):
            print("Wrong input in NaiveBayesClassifier.fit()")
        else:
            words_tags_count = {}
            self.tags_list = set(Y)
            # Getting word list from phrases given in X
            all_words = [word for phrase in X for word in phrase.split(" ") if word]
            self.words_list = set(all_words)
            tags_count = dict.fromkeys(self.tags_list, 0)
            for word in self.words_list:
                words_tags_count[word] = dict.fromkeys(self.tags_list, 0)
                self.words_prob[word] = dict.fromkeys(self.tags_list, 0)
            # Counting probability of all unique tags
            for tag in self.tags_list:
                prob = Y.count(tag)/len(Y)
                self.tags_prob[tag] = prob
            words_count = len(all_words)
            # Counting unique words for all tags
            for i in range(len(X)):
                for word in X[i].split(" "):
                    if word:
                        words_tags_count[word][Y[i]] += 1
                        tags_count[Y[i]] += 1
            # Counting probability of every word + tag combination
            for word in self.words_list:
                for tag in self.tags_list:
                    self.words_prob[word][tag] =\
                        (words_tags_count[word][tag] + self.alpha) / (tags_count[tag] + self.alpha * words_count)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predict_tags = []
        for phrase in X:
            predict_words_list = [word for word in phrase.split(" ") if word]
            ln_prob = {}
            for tag in self.tags_list:
                # print(self.tags_prob[tag])
                ln_prob[tag] = log(self.tags_prob[tag])
                # print(ln_prob[tag])
                for word in predict_words_list:
                    if word in self.words_list and self.words_prob[word][tag]:
                        ln_prob[tag] += log(self.words_prob[word][tag])
            predict_tags.append(max(ln_prob, key=(lambda key: int(ln_prob[key]))))
        return predict_tags

    def score(self, X_test, Y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        score = 0
        Y_predicted = self.predict(X_test)
        for i in range(len(Y_predicted)):
            if Y_predicted[i] == Y_predicted[i]:
                score += 1
        return int(score * 100 / len(Y_test))


if __name__ == "__main__":
    pass
