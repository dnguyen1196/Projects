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

# Also note to vary m from 0 to 0.9 and 1 to 10

# Note that if the overall vocabulary contains the word, must calculate the
# log likelihood, for the case of no smoothing, expect to have -Inf

class TYPE_I_CLASSIFIER:
    def __init__(self, train_index, test_index, folder):
        self.train_file = train_index # The index file contains training data
        self.test_file = test_index # Index file contains test data
        self.data_folder = folder # This is the directory containing all data folders

        # self.train_data = self.classifier_create_training_set(train_index)
        self.train_data = []

        self.VOCABULARY = {} # The vocabulary is to keep track
        # of which words are in the vocabulary, we need to know
        self.YES_VOCABULARY = {}
        # This shows the words and their frequency in the YES group and NO
        self.NO_VOCABULARY = {}

        # This refers to the number of documents classified as YES or NO
        self.YES_DOCUMENT_COUNT = 0
        self.NO_DOCUMENT_COUNT = 0
        # These refer to the total number of words in each YES or NO group
        self.YES_WORD_COUNT = 0
        self.NO_WORD_COUNT = 0


    # This function calls the function to first generate the overall training
    # set, it will the partition into 10 different training set size
    # of 0.1N, 0.2N, ... 1N
    # Size refers to the size of the training set that we are using
    # size must be between 0 and 1
    def classifier_train_and_test(self, size, m):
        # Create the training set
        # We do not have to repeat this step if all the lines in the
        # if (len(self.train_data) == 0):
        #     self.classifer_create_training_set()
        assert (size <= 1 and size > 0), 'Training set oversized'
        # If the training data does not already exist, create the training
        # data
        if (len(self.train_data) == 0):
            self.classifer_create_training_set()
        # Find the size of the training data
        N = len(self.train_data)
        # Choose the training set as a proportion of all given training data
        train_set = self.train_data[:int(size*N)]
        # Train on specific data set
        self.classifier_train_on_data(train_set)
        # Perform testing using laplace smoothing with parameter m
        accuracy = self.classifier_test(m)
        return accuracy

    # This function resets these learning parameters so the classifier can
    # learn from new data sets
    def classifier_untrain(self):
        self.VOCABULARY = {}
        self.YES_VOCABULARY = {}
        self.NO_VOCABULARY = {}

        self.YES_DOCUMENT_COUNT = 0
        self.NO_DOCUMENT_COUNT = 0

        self.YES_WORD_COUNT = 0
        self.NO_WORD_COUNT = 0


    # This return an array of lines from the train index file
    # we can separate the train index by proportion to generate the
    # learning curve by using sub arrays of this array
    def classifer_create_training_set(self):
        try:
            f = open(self.train_file, encoding='ISO-8859-1')
        except Exception as e:
            print (e)
        self.train_data = [line.rstrip("|\n") for line in f]


    # To improve modularity, this function trains on specific given data set
    def classifier_train_on_data(self, data):
        # Ensures that the classifier is untrained
        self.classifier_untrain()
        for line in data:
            (index, group) = line.split("|")
            # Get the filename
            filename = self.data_folder + index + ".clean"
            self.classifer_parse_document(filename, group)


    # This function parses the training document for specific words
    # It will add the words to the VOCABULARY if it's not already inside
    # It will increment the relevant YES or NO group word counts
    def classifer_parse_document(self, document, category):
        # For each word, if not in the dictionary, add one to the dictionary
        try:
            f = open(document, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        # Get the appropriate dictionary
        group_vocab = self.YES_VOCABULARY if category == "yes" else self.NO_VOCABULARY
        word_count = 0

        for line in f: # Parse each line in the document
            line = line.rstrip("\n").split()
            for token in line: # each token is a word in the document
                if (token):
                    if (token not in self.VOCABULARY):
                        self.VOCABULARY[token] = True

                    word_count += 1
                    if (token in group_vocab):
                        group_vocab[token] = group_vocab[token] + 1
                    else:
                        group_vocab[token] = 1
                    # Add the first instance into dict the new word to the vocabulary
                    if (token not in self.VOCABULARY):
                        self.VOCABULARY[token] = True

        # Update the total word count in each group's documents
        if (category == "yes"):
            self.YES_WORD_COUNT += word_count
            self.YES_DOCUMENT_COUNT += 1 # Update the number of YES and NO docs
        else:
            self.NO_WORD_COUNT += word_count
            self.NO_DOCUMENT_COUNT += 1

    # Function to test the classifier based on an index file of test data
    # To test on a new document, create a word vector of the document
    # For each word in the document, calculate the posterior probability
    # Remember to use log
    # m is the laplace smoothing parameters used
    def classifier_test(self, m):
        # Open the test test index file
        try:
            f = open(self.test_file, encoding='ISO-8859-1')
        except Exception as e:
            print (e)
        # Track the accuracy of classifications on the test set
        correct = 0
        count = 0
        for line in f:
            count += 1
            # Get the filename and the category
            (index, group) = line.rstrip("|\n").split("|")
            filename = self.data_folder + index + ".clean"
            category = self.classifer_classify_document(filename, m)
            if (group == category):
                correct += 1

        accuracy = float(correct)/count
        return accuracy

    # The function to classify the documents
    # This function calculates the posterior probability of each class
    # and returns the class with the higher probability
    def classifer_classify_document(self, document, m):
        # Find the log posterior probability
        log_poster_yes = self.find_log_posterior_probability(document, "yes", m)
        log_poster_no = self.find_log_posterior_probability(document, "no", m)

        if (log_poster_yes == -math.inf and log_poster_no == -math.inf):
            return "yes"
        return "yes" if log_poster_yes > log_poster_no else "no"

    # Function to calculate the posterior probability of a document
    # This function calculates the sum of log probability
    # It first calculates the prior probability and then adds the log
    # probability of the likelihood probability of each word in the document
    def find_log_posterior_probability(self, document, category, m):
        posterior_probability = 0.0
        # P (class) = len(self.YES) / len(self.NO) or vice versa
        prior_numerator = self.YES_DOCUMENT_COUNT if category == "yes" else self.NO_DOCUMENT_COUNT
        prior_probability = float(prior_numerator)/(self.YES_DOCUMENT_COUNT + self.NO_DOCUMENT_COUNT)
        posterior_probability += math.log2(prior_probability)

        # Try to open the document
        try:
            f = open(document, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        for line in f: # Parse each line in the document
            line = line.rstrip("\n").split()
            for token in line: # each token is a word
                if (token):
                    # Calculate the log likelihood of each word in category
                    log_likelihood = self.find_log_likelihood_probability(token, category, m)
                    posterior_probability += log_likelihood

        return posterior_probability


    # Function to find the log likelihood probability of a word given
    # a category in some documents
    def find_log_likelihood_probability(self, word, category, m):
        # (frequency of WORD in the group) + 1)
        # /(total numbe of words in all documents of the group) + |VOCABULARY|
        if (word not in self.VOCABULARY):
            return 0

        group_vocabulary = self.YES_VOCABULARY if category == "yes" else self.NO_VOCABULARY
        total_word_count = self.YES_WORD_COUNT if category == "yes" else self.NO_WORD_COUNT
        # If the word is NOT in the overall VOCABULARY, return 0 (equivalent
        # to skipping the word since it does not affect the log probability)
            # Apply laplace smoothing
        if (word in group_vocabulary):

            numerator = group_vocabulary[word] + m
        else:
            numerator = m

        denom = total_word_count + m * len(self.VOCABULARY) # The total vocabulary
        ratio = float(numerator)/denom
        if (ratio == 0):
            return -math.inf
        return math.log2(ratio)
