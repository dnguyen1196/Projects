import math
import random
# Type II classifier is based on the following formula
# #(w ^ c) + m
# / #c + mV
# w ^ c is the number of documents in class c that contains the word w
# So what do we need to do during training?
# Keep track of how many documents of certain class contains the word
# So the YES_VOCABULARY will contain words and the number of documents
# containing each word

# IMPORTANTNT
# Note that type II also takes into account the probability P (word is not in document | class)
# Need to change implementation abit -> also keep track of the order of the words in the vocabulary
# Need another array that keeps track of the order of the words


# Create another class variable called word vector that denotes all the words in the vocabulary in order
# Everytime we add a new word, append this word to the vocabulary array
# Keep the count within the YES_VOCABULARY and NO_VOCABULARY
# when testing a document, count the


class TYPE_II_CLASSIFIER:
    def __init__(self, train_file, test_file, folder):
        self.train_file = train_file
        self.test_file = test_file
        self.data_folder = folder

        self.train_data = []
        self.VOCABULARY = {} 
        self.word_array = [] # To create the binary

        self.YES_VOCABULARY = {}
        self.NO_VOCABULARY = {}

        self.YES_DOCUMENT_COUNT = 0
        self.NO_DOCUMENT_COUNT = 0

    # Perform training on a proportion of the total training set and
    # test the accuracy of Naive Bayes Type II with laplace smoothing parameter
    # m
    def classifier_train_and_test(self, size, m):
        # Create the training set
        assert (size <= 1 and size > 0), 'Training set oversized'
        if (len(self.train_data) == 0):
            self.classifier_create_training_set()
        # Find the size of the training data
        N = len(self.train_data)
        # Choose the training set as a proportion of all given training data
        train_set = self.train_data[:int(size*N)]
        # Train on the specific data set
        self.classifier_train_on_data(train_set)
        # Perform testing using laplace smoothing with parameter m and returns
        # the accuracy
        return self.classifier_test(m)

    def classifier_untrain(self):
        self.VOCABULARY = {}
        self.YES_VOCABULARY = {}
        self.NO_VOCABULARY = {}

        self.YES_DOCUMENT_COUNT = 0
        self.NO_DOCUMENT_COUNT = 0
        self.word_array = []

    def classifier_create_training_set(self):
        try:
            f = open(self.train_file, encoding='ISO-8859-1')
        except Exception as e:
            print (e)
        self.train_data = [line.rstrip("|\n") for line in f]

    # This allows us to specify what portion of the data
    def classifier_train_on_data(self, data):
        # Make sure that the classifier is untrained
        self.classifier_untrain()
        # Loop through each document in the given training data and parse the
        # document
        for line in data:
            (index, group) = line.split('|')
            document = self.data_folder + index + ".clean"
            self.classifier_parse_document(document, group)

        self.word_array = self.VOCABULARY.keys()
        # print (len(self.YES_VOCABULARY))
        # print (len(self.NO_VOCABULARY))
        # print (self.YES_DOCUMENT_COUNT)
        # print (self.NO_DOCUMENT_COUNT)
        # The word_array is the list of all the words in the VOCABULARY

    # Open a file and parse the necessary information
    def classifier_parse_document(self, document, group):
        try:
            f = open(document, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        # Keep track of which words we have seen to avoid double counting
        document_vocabulary = {}
        # We want to know how how many documents contain a specific words
        # If the word is not in the overall VOCABULARY, add it
        # For each document, keep track of which words we have come across
        # If we have come across it, it means we have already included it
        # in the VOCABULARY
        group_vocabulary = self.YES_VOCABULARY if group == "yes" else self.NO_VOCABULARY

        for line in f:
            line = line.rstrip("\n").split()
            for token in line:
                if (token):
                    # Add the word to the overall vocabulary if it's not already there
                    if (token not in self.VOCABULARY):
                        self.VOCABULARY[token] = True
                    # If we have checked this word, continue to avoid double counting
                    if (token in document_vocabulary):
                        continue
                    else: # We have not checked this word before
                        document_vocabulary[token] = True
                        if (token in group_vocabulary):
                            # Increase the number in the class that contains the word
                            group_vocabulary[token] = group_vocabulary[token] + 1
                        else:
                            # Add the first classified document that contains the word
                            group_vocabulary[token] = 1

        # Increase the DOCUMENT count of the specific class
        if (group == "yes"):
            self.YES_DOCUMENT_COUNT += 1
        else:
            self.NO_DOCUMENT_COUNT += 1


    # Perform test on the classifier, using laplace smoothing parameter m
    # Open the test file, browse through all the test document
    # This return the accuracy of the classifier
    def classifier_test(self, m):
        # Open the test index file
        try:
            f = open(self.test_file, encoding='ISO-8859-1')
        except Exception as e:
            print (e)
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
            # Testing purpose ################
        accuracy = float(correct)/count
        return accuracy

    # Perform classification on a specific document
    # Open the documents, calculate the necessary probability
    def classifer_classify_document(self, document, m):
        log_posterior_yes = self.find_log_posterior_probability(document, "yes", m)
        log_posterior_no = self.find_log_posterior_probability(document, "no", m)
        # If both log returns -infinity, return the class randomly
        # print (log_posterior_yes, " - ", log_posterior_no)
        if (log_posterior_yes == -math.inf and log_posterior_no == -math.inf):
            return "yes" if random.random() > 0.5 else "no"
        return "yes" if log_posterior_yes > log_posterior_no else "no"


    # To find the probability associated with a particular category, browse
    # through all the words in the document, and form a document_vocabulary
    # dictionary
    # Call another function that takes in this document_vocabulary and
    # calculate the sum of log probability based on the word_array
    def find_log_posterior_probability(self, document, category, m):
        prior_numerator = self.YES_DOCUMENT_COUNT if category == "yes" else self.NO_DOCUMENT_COUNT
        prior_denominator = self.YES_DOCUMENT_COUNT + self.NO_DOCUMENT_COUNT
        prior_probability = float(prior_numerator)/prior_denominator

        log_prior_probability = math.log2(prior_probability)
        try:
            f = open(document, encoding='ISO-8859-1')
        except Exception as e:
            print (e)

        # Create a dictionary to keep track of which word is present in the document
        document_vocabulary = {}
        for line in f:
            line = line.rstrip("\n").split()
            for token in line:
                if (token):
                    # Add word to the dictionary
                    if (token not in document_vocabulary):
                        document_vocabulary[token] = True

        log_likelihood = self.find_log_likelihood_probability(document_vocabulary, category, m)
        if (log_likelihood == -math.inf):
            return -math.inf
        return (log_prior_probability + log_likelihood)

    def find_log_likelihood_probability(self, document_vocabulary, category, m):
        group_vocabulary = self.YES_VOCABULARY if category == "yes" else self.NO_VOCABULARY
        group_document_count = self.YES_DOCUMENT_COUNT if category =="yes" else self.NO_DOCUMENT_COUNT

        denominator = group_document_count + m * 2
        # number of documents with or without word of specific class
        log_likelihood = 0.0
        # Go through the word array 1010101001111001, each document will be abstractly represented
        # as a binary sequence 10101010011111 (1 if the word is in the document, 0 if not)
        for word in self.word_array:
            # If the word is in the group vocabulary
            if (word in group_vocabulary):
                # If the word is in the document vocabulary, find the probability
                # a document in class c has the word
                if (word in document_vocabulary):
                    # Just the number of class c documents that have the word
                    numerator = group_vocabulary[word] + m
                else:
                    # find probability a document of class c does not have the word
                    # total number of documents - documents that have the word
                    numerator = group_document_count - group_vocabulary[word] + m
            # If the word is not in the group vocabulary
            else:
                # If the document contains the word but all other documents in the
                # that category does not
                if (word in document_vocabulary):
                    numerator = 0 + m
                else:
                    # If the document does not contain the word and other documents
                    numerator = group_document_count + m
            # if without laplace smoothing, and count = 0
            if (numerator == 0):
                return -math.inf
            else:
                # print (float(numerator)/denominator)
                log_likelihood += math.log2(float(numerator)/denominator)
                # print (math.log2(float(numerator)/denominator))
        return log_likelihood
