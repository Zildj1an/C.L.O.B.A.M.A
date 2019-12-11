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
filt2Alies = filtAlies.filter(lambda x: int(x.split(',')[18]) > 1850)
clearAlies = filt2Alies.map(lambda x : (((x.split(',')[3]) +", "+ (x.split(',')[18])), (x.split(',')[5])))
orderAlies = clearAlies.sortByKey()
AliesCountryAndYearS = orderAlies.reduceByKey(lambda x, y: x +", " +y) # date and Country in the same column

# GDP dataset cleanse

fileInput = "ProcessedDATAsets/GDPdef.csv"
textRDD = sc.textFile(fileInput)

def limpiarPrimeraLinea(line):
    if "country" in line:
        return False
    else:
        return True
        
def corregir(line):
    res = re.sub(r'"', '', line)
    return re.sub(r', ', ' ', line)

allGDP = textRDD.filter(lambda x: limpiarPrimeraLinea(x))
coregidaAllGDP = allGDP.map(lambda line: corregir(line))
filtgdp = coregidaAllGDP.filter(lambda x: int(x.split(',')[1]) > 1850)
gdp = coregidaAllGDP.map(lambda line: (str(line.split(',')[0]), int(line.split(',')[1]), int(line.split(',')[2])))
gdp = gdp.map(lambda line: (str(line[0]), (line[1], line[2])))
gdp = gdp.sortByKey()
gdpClaveFechaYNombre = gdp.map(lambda x:((x[0]+ ", "+ str(x[1][0])), x[1][1]))


#Inversion in war dataset cleanse

inversionFile ="ProcessedDATAsets/InviersonesDEF.csv"
RDDinversion = sc.textFile(inversionFile)
filtInversionRDD = RDDinversion.filter(lambda x: "country"  not in x)

cleanInversion = filtInversionRDD.map(lambda x: ((x.split(',')[0]+ ", "+ x.split(',')[1]), x.split(',')[2]))
sortedInversion = cleanInversion.sortByKey()

#Countries in war cleanse

CinwarFile = "ProcessedDATAsets/WarsPerYearDef.csv"
RDDContInWar = sc.textFile(CinwarFile)
filtContInWar = RDDContInWar.filter(lambda x: "country"  not in x)
MapContInWar = filtContInWar.map(lambda x: ((x.split(',')[0]+ ", " +x.split(',')[1]), 1))
SortedContInWar = MapContInWar.sortByKey()


#None to data functs

def NoneToNoAlies(x):
    if x is None:
        return ""
    else: return x
def NoneToNoGDP(x):
    if x is None:
        return 0
    else: return x

def NoneToNoGDPAllies(x):
    if x is None:
        return ("",0)
    else: return x
def NoneToZero(x):
    if x is None:
        return 0
    else: return x
    
def NoneToNoGDPAlliesInv(x):
    if x is None:
        return (("",0), 0)
    else: return x

def NoneToNoBorders(x):
    if x is None:
        return ""
    else: return x

#Data sets fusion

AliesJoinGdp = AliesCountryAndYearS.fullOuterJoin(gdpClaveFechaYNombre).map(lambda x: (x[0],(NoneToNoAlies(x[1][0]),NoneToNoGDP(x[1][1]))))


AliesGdpJoinInversion = AliesJoinGdp.fullOuterJoin(sortedInversion).map(lambda x: (x[0],( NoneToNoGDPAllies(x[1][0]), NoneToZero(x[1][1])) ))

AliesGdpInversionJoinInWar = AliesGdpJoinInversion.fullOuterJoin(SortedContInWar).map(lambda x: (x[0],( NoneToNoGDPAlliesInv(x[1][0]), NoneToZero(x[1][1]) )))

AliesGdpInversionJoinInWarClean = AliesGdpInversionJoinInWar.map(lambda x: (x[0].split(',')[0],  (x[0].split(',')[1].replace(' ',"") ,)+ x[1] ))

AliesGdpInversionJoinInWarJoinBorders = AliesGdpInversionJoinInWarClean.leftOuterJoin(Borders).map(lambda x: (x[0], x[1][0], NoneToNoBorders(x[1][1]) ))



FinalDataSet = AliesGdpInversionJoinInWarJoinBorders.map(lambda x:
(str('"' + x[0] + '"'),#COUNTRY
int(x[1][0]),#YEAR
str('"' + x[1][1][0][0] + '"'),#ALLIES
str('"' + x[2] + '"'),#BORDER COUNTRIES
float(x[1][1][1]),#INVERSION
int(x[1][1][0][1]),#GDP
int(x[1][2])) #WAR?
)


FilterData = FinalDataSet.filter(lambda x: (float(x[4]) >= 0.0)and(int(x[4]) != 0 and int(x[5]) != 0)  )

FilterData.saveAsTextFile("Join.txt")
