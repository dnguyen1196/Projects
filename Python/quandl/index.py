import sys
from simple_find import *


def main(argv):
    # For each company in the command line -> create a thread that gets the
    # stock data and perform optimization
    optimize_simple_portfolio(argv, 0)


if __name__ == "__main__":
   main(sys.argv[1:])
