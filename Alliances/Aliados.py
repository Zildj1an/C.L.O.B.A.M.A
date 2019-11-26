from pyspark import SparkConf, SparkContext
import string
import sys
import re

conf = SparkConf().setMaster('local').setAppName('Allies')
sc = SparkContext(conf = conf) 

RDDvar = sc.textFile("directed_yearly.csv") 
filt = RDDvar.filter(lambda l: "version4id" not in l)
clear = filt.map(lambda x : ((x.split(',')[2] +", "+ (x.split(',')[17])), (x.split(',')[4])))
orderData = clear.sortByKey()
reduce = orderData.reduceByKey(lambda x, y: x +", " +y)
reduce.saveAsTextFile("output.txt")