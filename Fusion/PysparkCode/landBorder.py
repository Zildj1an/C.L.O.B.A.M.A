from pyspark import SparkConf, SparkContext

import string
import sys
	
conf = SparkConf().setMaster('local').setAppName('landborder')
sc = SparkContext(conf=conf)
	
RDDvar = sc.textFile("CountryBorders.csv")
lineRDD = RDDvar.map(lambda country: ((country.split(",")[0].replace('"', "")), (country.split(",")[2]).replace('"', "")))
result = lineRDD.reduceByKey(lambda x,y : x +", "+ y)
result.saveAsTextFile("output1.txt")