from math import log


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.words_list = []
        self.words_prob = {}
        self.labels_list = []
        self.labels_prob = {}

    def fit(self, titles, labels):
        """ Fit Naive Bayes classifier according to titles, labels. """
        if len(titles) != len(labels):
            print("Wrong input in NaiveBayesClassifier.fit()")
        else:
            words_labels_count = {}
            self.labels_list.extend(set(labels))
            # Getting word list from phrases given in titles
            all_new_words = [word for phrase in titles for word in phrase.split(" ") if word]
            self.words_list.extend(set(all_new_words))
            labels_count = dict.fromkeys(self.labels_list, 0)
            for word in self.words_list:
                words_labels_count[word] = dict.fromkeys(self.labels_list, 0)
                self.words_prob[word] = dict.fromkeys(self.labels_list, 0)
            # Counting probability of all unique labels
            for label in self.labels_list:
                self.labels_prob[label] = labels.count(label)/len(labels)
            words_count = len(all_new_words)
            # Counting unique words for all labels
            for i in range(len(titles)):
                for word in titles[i].split(" "):
                    if word:
                        words_labels_count[word][labels[i]] += 1
                        labels_count[labels[i]] += 1
            # Counting probability of every word + label combination
            for word in self.words_list:
                for label in self.labels_list:
                    self.words_prob[word][label] = \
                        (words_labels_count[word][label] + self.alpha) / (labels_count[label] + self.alpha * words_count)
        return all_new_words, self.labels_list

    def predict(self, titles):
        """ Perform classification on an array of test vectors titles. """
        predict_labels = []
        for phrase in titles:
            predict_words_list = [word for word in phrase.split(" ") if word]
            ln_prob = {}
            for label in self.labels_list:
                # print(self.labels_prob[label])
                ln_prob[label] = log(self.labels_prob[label])
                # print(ln_prob[label])
                for word in predict_words_list:
                    if word in self.words_list and self.words_prob[word][label]:
                        ln_prob[label] += log(self.words_prob[word][label])
            predict_labels.append(max(ln_prob, key=(lambda key: int(ln_prob[key]))))
        return predict_labels

    def score(self, titles_test, labels_test):
        """ Returns the mean accuracy on the given test data and labels. """
        score = 0
        labels_predicted = self.predict(titles_test)
        for i in range(len(labels_predicted)):
            if labels_predicted[i] == labels_predicted[i]:
                score += 1
        return int(score * 100 / len(labels_test))


if __name__ == "__main__":
    pass
