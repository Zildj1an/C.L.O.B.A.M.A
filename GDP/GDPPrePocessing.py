import pandas as pd

def interpolar(i, data):
    nVeces = (data.at[i,'year'] - data.at[i - 1,'year'])
    media = (data.at[i, 'gdppc'] - data.at[i - 1, 'gdppc']) / nVeces
    acumulado = data.at[i - 1, 'gdppc']
    for j in range(0, nVeces):       
        acumulado += media
        data = data.append({'countrycode' : data.at[i, 'countrycode'], 'country' :data.at[i, 'country'], 'year' : data.at[i,'year'] + j , 'gdppc' : acumulado}, ignore_index=True)
    return data

data = pd.read_csv("GDPByCountry.csv")
res = pd.Dataframe(columns=['country', 'year'])

for i in range(2, len(data)):
    if(data.at[i-1, 'countrycode'] == data.at[i,'countrycode']):
        if ((data.at[i - 1,'year'] + 1 != data.at[i,'year']) and int(data.at[i - 1,'year']) >= 1850):
           data = interpolar(i, data)


data.to_csv("GDPDefPostPro.csv",index=False)