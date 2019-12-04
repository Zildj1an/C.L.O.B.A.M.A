
import pandas as pd


data1 = pd.read_csv("COW country codes.csv")
data = pd.read_csv("directed_yearly.csv")
for i in range(1,len(data1)):
    aux1 = data1.at[i,'StateNme']
    aux2 = data1.at[i,'StateAbb']
    print(aux1 + ' ')
    print(aux2 +'\n')
    data.replace(to_replace = aux1, value = aux2, inplace = True )
data.to_csv("AliadosProcesados.csv")
