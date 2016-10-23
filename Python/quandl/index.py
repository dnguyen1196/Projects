import sys
# import SimpleFind.simple_find as sf
import SparkQuandl.sparkquandl as sq

def main(argv):
    # portfolio = ["GOOGL", "FB", "TSLA"]
    # start = "2013-01-01"
    # end = "2015-12-31"
    #
    # results = sf.strategize_simple_find(portfolio, start, end)
    # while not results.empty():
    #     result = results.get()
    #     print (result[0], result[4])
    sq.test("./result.txt")

if __name__ == "__main__":
   main(sys.argv[1:])
