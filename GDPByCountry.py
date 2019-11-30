from pyspark import SparkConf, SparkContext, sql
from pyspark.sql import SQLContext, functions
import string
import re



conf = SparkConf().setMaster('local').setAppName('P1_Spark')
sc = SparkContext(conf = conf)
fileInput = "GDPByCountry.csv"
textRDD = sc.textFile(fileInput)

def limpiarPrimeraLinea(line):
    if "gdppc" in line:
        return False
    else:
        return True
        
def corregir(line):
    res = re.sub(r'"', '', line)
    return re.sub(r', ', ' ', line)

allGDP = textRDD.filter(lambda x: limpiarPrimeraLinea(x))
coregidaAllGDP = allGDP.map(lambda line: corregir(line))
gdp = coregidaAllGDP.map(lambda line: (str(line.split(',')[1]), int(line.split(',')[2]), int(line.split(',')[3])))
gdp.saveAsTextFile("output")


