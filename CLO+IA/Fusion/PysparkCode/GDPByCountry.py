from pyspark import SparkConf, SparkContext, sql
from pyspark.sql import SQLContext, functions
import string
import re



conf = SparkConf().setMaster('local').setAppName('P1_Spark')
sc = SparkContext(conf = conf)
fileInput = "../ProcessedDATAsets/GDPDefPostPro.csv"
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
gdp = coregidaAllGDP.map(lambda line: (str(line.split(',')[0]), int(line.split(',')[2]), int(line.split(',')[3])))
gdp = gdp.map(lambda line: (str(line[0]), (line[1], line[2]))).sortByKey()
gdp.saveAsTextFile("output.csv")
#gdp.coalesce(1).write.format("com.databricks.spark.csv").mode("overwrite").option("header", "true").save("output2.csv")