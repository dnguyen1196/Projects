import sys

from type_I_naivebayes import *
from type_II_naivebayes import *

# Read the data from the test_train file
# For each file, create a word vector representation of the file
# Do precalculations on the word vector

if __name__ == "__main__":
    class_I = TYPE_I_CLASSIFIER("./pp2data/ibmmac/index_train", "./pp2data/ibmmac/index_test","./pp2data/ibmmac/")
    class_I.classifier_train()
    class_I.classifier_test()
