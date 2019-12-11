
import pandas as pd


data1 = pd.read_csv("Acronimos.csv")
data = pd.read_csv("CountryBorders.csv")
for i in range(1,len(data1)):
    aux1 = data1.at[i,'Two_Letter_Country_Code']
    aux2 = data1.at[i,'Three_Letter_Country_Code']
    data.replace(to_replace = aux1, value = aux2, inplace = True )
data.to_csv("CountryBordersProcessed.csv")
