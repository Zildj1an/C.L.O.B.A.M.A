from pyspark import SparkConf, SparkContext
import string
import sys
import re


conf = SparkConf().setMaster('local').setAppName('Allies')
sc = SparkContext(conf = conf) 




RDDvar = sc.textFile("AliadosProcesados.csv")
filt = RDDvar.filter(lambda l: "version4id" not in l)
clear = filt.map(lambda x : (((x.split(',')[3]) +", "+ (x.split(',')[18])), (x.split(',')[5])))



orderData = clear.sortByKey()
separate = orderData.map(lambda x: (x[0].split(',')[0], x[0].split(',')[1].replace(' ', ""), x[1] ))

reduce = orderData.reduceByKey(lambda x, y: x +", " +y)
noAcr = reduce.map(lambda x: (x[0].split(',')[0], x[0].split(',')[1].replace(' ', ""), x[1] ))

noAcr.saveAsTextFile("output.txt")