from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions
import string
import sys
import re

conf = SparkConf().setMaster('local').setAppName('warData')
sc = SparkContext(conf=conf)



# Border dataset cleanse
RDDBorders = sc.textFile("ProcessedDATAsets/CountryBordersProcessed.csv")
filteBorders = RDDBorders.filter(lambda x: "Country1" not in x)
lineRDDBorders = filteBorders.map(lambda country: ((country.split(",")[1].replace('"', "")), (country.split(",")[3]).replace('"', "")))
Borders = lineRDDBorders.reduceByKey(lambda x,y : x +", "+ y)

# Alies dataset cleanse

RDDAlies = sc.textFile("ProcessedDATAsets/AliadosProcesadosV2.csv")
filtAlies = RDDAlies.filter(lambda l: "version4id" not in l)
clearAlies = filtAlies.map(lambda x : (((x.split(',')[3]) +", "+ (x.split(',')[18])), (x.split(',')[5])))
orderAlies = clearAlies.sortByKey()
AliesCountryAndYearS = orderAlies.reduceByKey(lambda x, y: x +", " +y) # date and Country in the same column

# GDP dataset cleanse

fileInput = "ProcessedDATAsets/GDPDefPostPro.csv"
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
gdpClaveFechaYNombre = gdp.map(lambda x:((x[0]+ ", "+ str(x[1][0])), x[1][1]))


#Inversion in war dataset cleanse

inversionFile ="ProcessedDATAsets/gdppercent.csv"
RDDinversion = sc.textFile(inversionFile)
filtInversionRDD = RDDinversion.filter(lambda x: "country"  not in x)
cleanInversion = filtInversionRDD.map(lambda x: ((x.split(',')[0]+ ", "+ x.split(',')[1]), x.split(',')[2]))
sortedInversion = cleanInversion.sortByKey()

#Countries in war cleanse

CinwarFile = "ProcessedDATAsets/WarsPerYearProcessed.csv"
RDDContInWar = sc.textFile(CinwarFile)
filtContInWar = RDDContInWar.filter(lambda x: "country"  not in x)
MapContInWar = filtContInWar.map(lambda x: ((x.split(',')[1]+ ", " +x.split(',')[2]), 1))
SortedContInWar = MapContInWar.sortByKey()


#None to data functs

def NoneToNoAlies(x):
    if x is None:
        return "NoAllies"
    else: return x
def NoneToNoGDP(x):
    if x is None:
        return 0
    else: return x

def NoneToNoGDPAllies(x):
    if x is None:
        return ("NoAllies",0)
    else: return x
def NoneToZero(x):
    if x is None:
        return 0
    else: return x
def NoneToNoGDPAlliesInv(x):
    if x is None:
        return (("NoAllies",0), 0)
    else: return x

def NoneToNoBorders(x):
    if x is None:
        return "NoBorders"
    else: return x

#Data sets fusion

AliesJoinGdp = AliesCountryAndYearS.fullOuterJoin(gdpClaveFechaYNombre).map(lambda x: (x[0],(NoneToNoAlies(x[1][0]),NoneToNoGDP(x[1][1]))))


AliesGdpJoinInversion = AliesJoinGdp.fullOuterJoin(sortedInversion).map(lambda x: (x[0],( NoneToNoGDPAllies(x[1][0]), NoneToZero(x[1][1])) ))

AliesGdpInversionJoinInWar = AliesGdpJoinInversion.fullOuterJoin(SortedContInWar).map(lambda x: (x[0],( NoneToNoGDPAlliesInv(x[1][0]), NoneToZero(x[1][1]) )))

AliesGdpInversionJoinInWarClean = AliesGdpInversionJoinInWar.map(lambda x: (x[0].split(',')[0],  (x[0].split(',')[1].replace(' ',"") ,)+ x[1] ))

AliesGdpInversionJoinInWarJoinBorders = AliesGdpInversionJoinInWarClean.leftOuterJoin(Borders).map(lambda x: (x[0], x[1][0], NoneToNoBorders(x[1][1]) ))


FinalDataSet = AliesGdpInversionJoinInWarJoinBorders.map(lambda x: (x[0], x[1][0], x[1][1][0][0], x[2], x[1][1][1], x[1][1][0][1], x[1][2]))


FinalDataSet.saveAsTextFile("Join.txt")
