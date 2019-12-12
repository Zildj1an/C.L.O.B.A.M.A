import pandas as pd

data = pd.read_csv("GDPByCountry.csv")

def interpolar(i, data):
    nVeces = (data.at[i,'year'] - data.at[i - 1,'year'])
    media = (data.at[i, 'gdppc'] - data.at[i - 1, 'gdppc']) / nVeces
    acumulado = data.at[i - 1, 'gdppc']
    for j in range(0, nVeces):       
        acumulado += media
        data = data.append({'countrycode' : data.at[i, 'countrycode'], 'country' :data.at[i, 'country'], 'year' : data.at[i,'year'] + j , 'gdppc' : 		acumulado}, ignore_index=True)
    return data

def interpolar2(i, data):
    num = (2020 - data.at[i - 1, 'year'])
    suma = (data.at[i - 2, 'gdppc'] - data.at[i - 1, 'gdppc'])
    acumulado = data.at[i - 1, 'gdppc']
    for j in range(1, num): 
	acumulado += suma
	data = data.append({'countrycode' : data.at[i - 1, 'countrycode'], 'country' :data.at[i - 1, 'country'], 'year' : data.at[i - 1,'year'] + j , 		'gdppc' : acumulado}, ignore_index=True)
    return data
   
for i in range(2, len(data)):
    if(data.at[i-1, 'countrycode'] == data.at[i,'countrycode']):
        if ((data.at[i - 1,'year'] + 1 != data.at[i,'year']) and int(data.at[i - 1,'year']) >= 1850):
           data = interpolar(i, data)

    if(data.at[i-1, 'countrycode'] != data.at[i,'countrycode']):
	if(data.at[i - 1,'year'] < 2019):
	   data = interpolar2(i, data)
res = pd.DataFrame(columns=['Country','Year', 'gdppc'])

for i in range(1, len(data)):

    res = res.append({'Country' : data.at[i, 'countrycode'], 'Year' : data.at[i, 'Year'], 'gdppc' : data.at[i, 'gdppc']},ignore_index=True)

res.sort_values(by=['Country', 'Year'], inplace=True)

res.to_csv("GDPFIN.csv",index=False)
data.to_csv("GDPDefPostPro.csv",index=False)
