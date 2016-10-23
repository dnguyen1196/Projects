from pyspark import SparkContext

def test(filename):
    sc = SparkContext()
    words = sc.textFile(name=filename)
