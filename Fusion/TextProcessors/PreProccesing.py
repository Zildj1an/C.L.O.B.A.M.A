import pandas as pd
import numpy as np
import re
import os

def limpiar(st):
    #p = re.split(r'\(|\)', st)[1]
    prueba = re.search(r'\((.*?)\)',st).group(1)
    num = re.split(r'-', prueba)
    if len(num) > 1:
        if len(num[1]) == 2:
            num1 = str(num[0])
            numCor = num1[0] + num1[1] + str(num[1])
            return [num1, numCor]
        else:
            return [str(num[0]), str(num[1])]
    else:
        return [str(num[0])]

res = pd.DataFrame(columns=['country','year'])

limite = 1850


#r',(?! )|,"|",'
files = os.listdir("Wars/")
fileNames = []
for file in files:
    if(file.endswith('.csv')):
        fileNames.append("Wars/" + file)
for fileAct in fileNames:
    print(fileAct + "\n")
    a = re.split(r'/', str(fileAct))[1]
    acronimo = re.sub(r'.csv', '', a)
    print(acronimo + "---\n\n\n")
    data = pd.read_csv(fileAct, engine='python', usecols=[0])
    for i in range(0, len(data)):
       
        country_year = data.iloc[i, 0]
        numerosAPars = limpiar(country_year)
        print(numerosAPars)
        if len(numerosAPars) == 1:
            try:
                numAux = int(numerosAPars[0])
                print(numAux)
                if numAux >= limite:
                    res = res.append({'country' : acronimo, 'year' : str(numAux)},ignore_index=True)
            except:
                print("Error converting int")
        else:
            print("antes del try\n\n")
            try:
                print(numerosAPars[0] + "->")
                year1 = int(numerosAPars[0])
                year1 = max(year1, limite)
                year2 = int(numerosAPars[1] + "")
                print(year1)
                print(year2)
                if year1 <= year2:
                    print("meto en res\n\n")
                    res = res.append({'country' : acronimo, 'year' : str(year1)},ignore_index=True)
                    for j in range(year2 - year1):
                        res = res.append({'country' : acronimo, 'year' : str(year1 + j)},ignore_index=True)
                    
                    res = res.append({'country' : acronimo, 'year' : str(year2)},ignore_index=True)

            except:
                print("Error converting int")
    data.drop(data.columns, axis=1)

res.sort_values(by=['country', 'year'], inplace=True)

res.drop_duplicates(subset=['country', 'year'], keep='first', inplace=True)

res.to_csv("WarsPerYearDef.csv",index=False)