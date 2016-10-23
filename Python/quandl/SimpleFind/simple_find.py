import quandl
import threading
import queue

# QUANDL API_KEY
quandl.api_key = 'wvMUzzkjBgybjKKuPZVK'

# A suite of functions that finds the optimal long/short strategy by
# using Kadane's algorithm to find the maximum subsequence and minimum
# subsequence

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
    for i in range(len(arr)): # Go through each element and add to the sum
        cur_sum = cur_sum + arr[i]
        if (cur_sum < 0): # If the current sum becomes 0, we can still be sure
            cur_sum = 0
            cur_start = i+1 # Don't have to worry about out of bound as i will
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


# optimal_long_simple_find(stock, start, end)
#   Input: stock name, start date and end date
#   Return: the optimal start and end date and the total profit made
def optimal_long_simple_find(results, stock, start, end):
    try:
        data = quandl.get(stock, start_date=start, end_date=end, collapse="daily")
        prices = data.as_matrix(['Adj. Close'])
        dates = data.index.values
        (longst, longend, longtot) = optimal_long_find(prices)
        (shortst, shortend, shorttot) = optimal_short_find(prices)
        if (longtot > shorttot):
            results.put(("long", stock, dates[longst], dates[longend], longtot))
        else:
            results.put(("short", stock, dates[shortst], dates[shortend], shorttot))
    except Exception as e:
        pass


# strategize_simple_find()
#   Input: portfolio (array of stock names), start date, enddate
#   Output: return the results for each stock, "long/short", stock name, start end date
#           and total profit earned
def strategize_simple_find(portfolio, startdate, enddate):
    threads = []
    results = queue.Queue()
    try:
        for name in portfolio:
            stock = "WIKI/" + name
            opt = threading.Thread(target=optimal_long_simple_find, args=(results, stock, startdate, enddate))
            threads.append(opt)
        for opt in threads:
            opt.start()

        for thread in threads:
            thread.join()

        return results
    except Exception as e:
        print(e)


