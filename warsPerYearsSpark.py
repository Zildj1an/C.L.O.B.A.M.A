from pyspark import SparkConf, SparkContext
import string
import re


conf = SparkConf().setMaster('local').setAppName('P1_Spark')
sc = SparkContext(conf = conf)

fileInput = "WarsPerYears.csv"
textRDD = sc.textFile(fileInput)

def quitar1Linea(line):
    if "CHRONOLOGICAL LIST OF ALL WARS" in line:
        return False
    else:
        return True


#solo si es necesario limpiar los datos
def limpiezaDeDatos(line):
    m = re.search(r'^\d{3}[0-9]', line)
    if m != None:
        return m.group(0)



years = textRDD.filter(lambda line: quitar1Linea(line)).map(lambda line: line.split(',')[0])
print(years.collect())
years.saveAsTextFile("output.txt") #a mi no me guarda los datos, pero si que salen bien por pantalla
