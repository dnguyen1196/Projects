import math
import numpy as np
import matplotlib.pyplot as plt
import sys

# The performance of J48 that was recorded using weka command line tool
j48_performance = {"ionosphere_test.arff":91.453, "irrelevant_test.arff":64.5, "mfeat-fourier_test.arff":74.6627, "spambase_test.arff":91.5906}

# This global array contains the features and their information gain
# To be initialized when we select the features
FEATURE_INFO_GAIN =[]

# Function to generate data set from arff file
def generateDataSet(filename):
	try:
		f = open(filename)
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		sys.exit(1)

	data = []
	for line in f:
		line = line.rstrip('\n')
		# Start reading data after we reach this marker
		if (line == "@data" or line =="@DATA"):
			break

	for line in f:
		line = line.rstrip('\n')
		token = line.split(",")
		size = len(token)
		category = token[size-1] #Get the class
		features = [float(i) for i in token[:size-1]]
		instance = Instance(features, category)
		data.append(instance)

	return data

# The class Instance that contains the category and array of feature
# values
class Instance:
	def __init__(self, feat, cate):
		self.features = feat
		self.category = cate

# Function to perform kNN that takes in the training data, test data, 
# number of neighbors and number of features during feature selection
def performkNN(train_data, test_data, k, num):
	if (num != None):
		weights = featureSelection(train_data, num)
	 # If number of features is not specify, use all features
	else:
		weights = np.ones(len(train_data[0].features))

	correct = 0.0
	for test in test_data:
		category = generateClass(train_data, test, k, weights)
		actual = test.category
		if (category == actual):
			correct = correct + 1

	accuracy = correct/(float)(len(test_data))
	return accuracy

# Perform feature selection
def featureSelection(train_data, num):
	num_features = len(train_data[0].features)
	weights = np.zeros(num_features)
	global FEATURE_INFO_GAIN 

	# Go through all the features and calculate the gain
	# For the same data set, we only have to do this only once
	if (len(FEATURE_INFO_GAIN) == 0):
		for i in range(num_features):
			gain = calculateGain(train_data, i)
			FEATURE_INFO_GAIN.append((i, gain))
	# Sort the features by the order of greatest info gain to smallest
		FEATURE_INFO_GAIN.sort(key=lambda x:x[1], reverse=True)  
	
	# If we already have a sorted FEATURE_INFO_GAIN
	for i in range(num):
		(index, gain) = FEATURE_INFO_GAIN[i]
		weights[index] = 1

	return weights

# Calculate the information gain when using a particular feature
def calculateGain(train_data, i):
	# Sort the train data by feature
	train_data.sort(key = lambda x: x.features[i])
	num_instances = len(train_data)

	entropy_before = findEntropy(train_data, 0, num_instances)
	entropy_after = 0.0

	group_size = (int) (num_instances/5) #Divide the data set into 5 groups
	for i in range(4):
		ratio = (float)(group_size)/num_instances
		entropy_after += ratio * findEntropy(train_data, i*group_size, (i+1)*group_size)

	ratio = (float)(num_instances - i*group_size)/num_instances
	entropy_after += findEntropy(train_data, i*group_size, num_instances) * ratio
	return (entropy_before - entropy_after)

# Find the entropy within a given data set in range lo to hi
def findEntropy(train_data, lo, hi):
	class_count = {}
	for i in range(lo, hi):
		point = train_data[i]
		category = point.category
		if (category in class_count):
			count = class_count[category]
			count = count + 1
			class_count[category] = count # Update class count
		else:
			class_count[category] = 1 # First instance of class

	entropy = 0.0
	total = hi - lo
	for count in class_count.values():
		p = (float)(count)/total
		entropy = entropy - p* math.log(p, 2)

	return entropy


# Function to predict the class of an instance based on the train
# data
def generateClass(train_data, data, k, weights):
	distances = []
	for ref in train_data:
		dist = calculateDistance(ref, data, weights)
		category = ref.category
		distances.append((dist, category))

	# Sort the distances array
	distances.sort(key=lambda tup: tup[0])
	category = generateClassFromArray(distances, k)
	return category
	
# Function to generate the class of the array of euclidean distances
# Select the most prevalent class among the nearest k neighbors
def generateClassFromArray(distances, k):
	classification = {}
	dom_count = 0 #The dominant class and most count
	dom_class = None
	# Find the class that recurs the most
	for i in range(k):
		(dist, category) = distances[i]
		if (category in classification):
			count = classification[category]
			count = count + 1
			if (count > dom_count):
				dom_count = count
				dom_class = category
			classification[category] = count
		else:
			classification[category] = 1

	return dom_class

# Calculate the euclidean distance between two data instances
# Take into account the weights of specific features
def calculateDistance(reference, data, weights):
	ref_features = reference.features
	data_features = data.features
	size = len(ref_features)
	distance = 0.0
	for i in range(size):
		distance += weights[i] * ((ref_features[i] - data_features[i])**2)

	return math.sqrt(distance)

# Functions to plot accuracy against k neighbors
def plotAccuracyAgainstK(accuracies, J48_result, test_file):
	x = range(1,26)
	plt.figure(figsize=(10,6))
	plt.plot(x, accuracies, label="kNN")
	plt.axhline(J48_result, label="J48", color="red")
	plt.ylabel("accuracy")
	plt.xlabel("number of neighbors")
	plt.ylim(0,100)
	title = "Performance on " + test_file
	plt.title(title)
	plt.legend(bbox_to_anchor=(1.05, 1), loc=5, borderaxespad=0.)

	tokens = test_file.split("_")
	newname = tokens[0] + "_performance.pdf"
	plt.savefig(newname)

# Function to plot accuracy against n features
def plotAccuracyAgainstNfeat(accuracies, J48_result, test_file):
	num_features = len(accuracies)
	x = range(1, num_features+1)
	plt.figure(figsize=(10,6))
	plt.plot(x, accuracies, label="kNN")
	plt.axhline(J48_result, label="J48", color="red")
	plt.ylim(0,100)
	plt.ylabel("accuracy")
	plt.xlabel("number of features")

	title = "Performance on " + test_file
	plt.title(title)
	plt.legend(bbox_to_anchor=(1.05, 1), loc=5, borderaxespad=0.)
		
	tokens = test_file.split("_")
	newname = tokens[0] + "_feature_select.pdf"
	plt.savefig(newname)

def usage():
	print "Correct usage: $ python kNN -t <train_data.arff> -T <test_data.arff>"

def main(argv):
	try:
		if (argv[0] != "-t" or argv[2] != "-T"):
			usage()
			sys.exit(1)
	except IndexError:
		usage()
		sys.exit(1)

	train_file = argv[1] #Get the file names
	test_file = argv[3]
	#Open and generate the data sets
	train_data = generateDataSet(train_file) 
	test_data = generateDataSet(test_file)

	accuracies = []
	for k in range(1,26): #Vary k neighbors from 1 to 25
		accuracy = performkNN(train_data, test_data, k, None)
		accuracies.append(accuracy*100) #In percentage

	plotAccuracyAgainstK(accuracies, j48_performance[test_file], test_file)

	accuracies = []
	num_features = len(train_data[0].features) # Get the number of features
	for num in range(1, num_features+1): # Vary feature selection from 1 to all features
		accuracy = performkNN(train_data, test_data, 5, num) # Set k = 5
		accuracies.append(accuracy*100)
	plotAccuracyAgainstNfeat(accuracies, j48_performance[test_file], test_file)

if __name__ == '__main__':
	main(sys.argv[1:])
	sys.exit(0)
	
