import math
# Bayes classifier works by finding the class with the highest
# P(class | Data) = P(Data| class) * P(class)
# Type 1: each document is a word vector in which each index is a word
# P(class | data) = π P(word_j = "word"| class) * P(class)

# Need to do some precalculations

# The data structure to store the relevant information

# Function that takes in the index file + folder of the datasets
# Output is a data structure that contains the training data and
# relevant probability information

class TYPE_I_CLASSIFIER:
    def __init__(self, train_index, test_index, dataset):
        self.train = train_index # The index file contains training data
        self.test = test_index # Index file contains test data
        self.data = dataset # This is the directory containing all data folders

        self.VOCABULARY = {} # The vocabulary is to keep track
        # of which words are in the vocabulary, we need to know
        self.YES_VOCABULARY = {} # This shows the frequency of words
        self.NO_VOCABULARY = {}

        # This refers to the number of documents classified as YES or NO
        self.YES_GROUP_SIZE = 0
        self.NO_GROUP_SIZE = 0
        # These refer to the total number of words in each YES or NO group
        self.YES_GROUP_WORD_COUNT = 0
        self.NO_GROUP_WORD_COUNT = 0

    # This function uses the train index and the data folder to
    # generate

    # Create functions that separate the training set into groups
    def classifier_train(self):
        # Read the train_index file
        try:
            f = open(self.train, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        for line in f:
            (index, group) = line.rstrip("|\n").split("|")
            # Get the filenme
            filename = self.data + index + ".clean"
            self.classifer_parse_document(filename, group)

    # The parse function opens a file and read word by word from the file
    # GROUP_NO and GROUP_YES are two dictionaries that contain the frequencies
    # of the words found in all the training data sets
    # Note that the final calculations of Naive bayes requires the frequency
    # of a specific word in all the training data
    # The total number of length of all the documents -> so we can keep track
    # of that -> keep it as an instance variable


    def classifer_parse_document(self, filename, category):
        # For each word, if not in the dictionary, add one to the dictionary
        try:
            f = open(filename, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        # Get the appropriate dictionary
        group_vocab = self.YES_VOCABULARY if category == "yes" else self.NO_VOCABULARY
        word_count = 0

        for line in f: # Parse each line in the document
            line = line.rstrip("\n").split()
            for token in line: # each token is a word in the document
                if (token):
                    word_count += 1
                    if (token in group_vocab):
                        group_vocab[token] = group_vocab[token] + 1
                    else:
                        group_vocab[token] = 1 # Add the first instance into dict
                    # Add the new word to the vocabulary
                    if (token not in self.VOCABULARY):
                        self.VOCABULARY[token] = True

        # Update the total word count in each group's documents
        if (category == "yes"):
            self.YES_GROUP_WORD_COUNT += word_count
            self.YES_GROUP_SIZE += 1 # Update the number of YES and NO docs
        else:
            self.NO_GROUP_WORD_COUNT += word_count
            self.NO_GROUP_SIZE += 1

    # Function to test the classifier based on an index file of test data
    # To test on a new document, create a word vector of the document
    # For each word in the document, calculate the posterior probability
    # Remember to use log
    def classifier_test(self):
        # Open the test test index file
        try:
            f = open(self.test, encoding='ISO-8859-1')
        except Exception as e:
            print (e)
        # Track the accuracy of classifications on the test set
        correct = 0
        count = 0
        for line in f:
            count += 1
            (index, group) = line.rstrip("|\n").split("|")
            # Get the filenme
            filename = self.data + index + ".clean"
            category = self.classifer_classify_document(filename)
            if (group == category):
                correct += 1

        accuracy = float(correct)/count
        print (accuracy)
        return accuracy

    def classifer_classify_document(self, document):
        # Find the log posterior probability
        log_poster_yes = self.find_log_posterior_probability(document, "yes")
        log_poster_no = self.find_log_posterior_probability(document, "no")
        return "yes" if log_poster_yes > log_poster_no else "no"

    def find_log_posterior_probability(self, document, category):
        posterior_probability = 0.0
        # P (class) = len(self.YES) / len(self.NO) or vice versa
        prior_numerator = self.YES_GROUP_SIZE if category == "yes" else self.NO_GROUP_SIZE
        prior_probability = float(prior_numerator)/((self.YES_GROUP_SIZE) + self.NO_GROUP_SIZE)
        posterior_probability += math.log2(prior_probability)

        try:
            f = open(document, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        for line in f: # Parse each line in the document
            line = line.rstrip("\n")
            try:
                line = line.split()
            except Exception as e:
                continue # Skip the line if some characters are unrecognizable

            for token in line: # each token is a word
                if (token):
                    # Calculate the log likelihood of each word in category
                    log_likelihood = self.find_log_likelihood_probability(token, category)
                    posterior_probability += log_likelihood

        return posterior_probability

    def find_log_likelihood_probability(self, word, category):
        # (frequency of WORD in the group) + 1)
        # /(total numbe of words in all documents of the group) + |VOCABULARY|
        vocabulary = self.YES_VOCABULARY if category == "yes" else self.NO_VOCABULARY
        total_word_count = self.YES_GROUP_WORD_COUNT if category == "yes" else self.NO_GROUP_WORD_COUNT

        # If the word is NOT in the overall VOCABULARY, return 0 (equivalent
        # to skipping the word since it does not affect the log probability)
        if (word in self.VOCABULARY):
            # Apply laplace smoothing
            if (word in vocabulary):
                frequency = vocabulary[word] + 1
            else:
                frequency = 1
        else:
            return 0
        denom = total_word_count + len(self.VOCABULARY) # The total vocabulary
        ratio = float(frequency)/denom
        return math.log2(ratio)
