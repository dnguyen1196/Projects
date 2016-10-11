import quandl
import numpy
import pandas
import time
import threading
import sys

from simple_find import *

# QUANDL API_KEY
quandl.api_key = 'wvMUzzkjBgybjKKuPZVK'

# Function to perform find the best short/ long stategy for a specific
# stock
# Takes in (name, date start, date end)
# Returns best short strategy + best long strategy
def optimal_long_simple_find(stock, start, end):
    try:
        data = quandl.get(stock, start_date=start, end_date=end, collapse="daily")
        prices = data.as_matrix(['Adj. Close'])
        dates = data.index.values
        (start, end, total) = optimal_long_find(prices)
        print ("Stock: ", stock, " profit: ", total)
        return (dates[start], dates[end], total)
    except Exception as e:
        pass # Just skip for whatever the stock name is incorrect

# Create a function that takes in a series of stock name and concurrently
# Run the getting data + analysis

def main(argv):
    # For each company in the command line -> create a thread that gets the
    # stock data and perform optimization
    threads = []
    # How to create a command line system that also includes -t option on time
    try:
        for name in argv:
            stock = "WIKI/" + name
            opt = threading.Thread(target=optimal_long_simple_find, args=(stock, "2013-01-01", "2014-12-31"))
            threads.append(opt)
        for opt in threads:
            opt.start()
    except Exception as e:
        print (e)


if __name__ == "__main__":
   main(sys.argv[1:])
