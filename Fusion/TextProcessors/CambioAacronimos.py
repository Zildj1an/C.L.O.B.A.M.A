
import pandas as pd


data1 = pd.read_csv("../CountryNamesTable/COW country codes.csv")
data = pd.read_csv("../WarsPerYearDef.csv")
for i in range(1,len(data1)):
    aux1 = data1.at[i,'StateAbb']
    aux2 = data1.at[i,'TrueAbb']
    print(aux1 + ' ')
    print(aux2 +'\n')
    data.replace(to_replace = aux1, value = aux2, inplace = True )
data.to_csv("WarsPerYearProcessed.csv")