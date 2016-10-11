import quandl
import numpy
import pandas
import threading

quandl.ApiConfig.api_key = 'wvMUzzkjBgybjKKuPZVK'

# Use kadane's algorithm
# Convert the array into an array of differences
def optimal_long_find(arr):
    differences = [] # Convert the original array into an array of differences
    for i in range(1, (len(arr))):
        differences.append(arr[i]-arr[i-1])
    (start, end, total) = max_subsequence_find(differences)
    return (start, end+1, total)

def optimal_short_find(arr):
    differences = []
    for i in range(1, len(arr)):
        differences.append(arr[i] - arr[i-1])
    (start, end, total) = min_subsequence_find(differences)
    return (start, end+1, total)

def max_subsequence_find(arr):
    best_start = 0
    best_end = 0
    best_sum = 0

    cur_sum = 0
    cur_start = 0
    cur_end = 0
    for i in range(len(arr)): # Go through each element and add to the sum
        cur_sum = cur_sum + arr[i]
        if (cur_sum < 0): # If the current sum becomes 0, we can still be sure
        # that we have kept the best sum and best start somewhere
            cur_sum = 0
            cur_start = i+1 # Don't have to worry about out of bound as i will
            # get incremented at the end anyway
        if (cur_sum > best_sum):
            best_start = cur_start
            best_end = i
            best_sum = cur_sum

    return (best_start, best_end, best_sum)


def min_subsequence_find(arr):
    best_start = 0
    best_end = 0
    best_sum = 0

    cur_sum = 0
    cur_start = 0
    cur_end = 0
    for i in range(len(arr)):
        cur_sum = cur_sum + arr[i]
        if (cur_sum > 0):
            cur_sum = 0
            cur_start = i+1
        if (cur_sum < best_sum):
            best_start = cur_start
            best_sum = cur_sum
            best_end = i
    return (best_start, best_end, best_sum)


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
        return (dates[start], dates[end], total)
    except Exception as e:
        print ("Wrong stock name: ", e)
        pass

# Create a function that takes in a series of stock name and concurrently
# Run the getting data + analysis

def optimize_simple_portfolio(portfolio, time):
    threads = []
    try:
        for name in portfolio:
            stock = "WIKI/" + name
            opt = threading.Thread(target=optimal_long_simple_find, args=(stock, "2013-01-01", "2014-12-31"))
            threads.append(opt)
        for opt in threads:
            opt.start()
    except Exception as e:
        print ("Exception: ", e)
