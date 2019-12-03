import pandas as pd 

dataEX = pd.read_csv("COW_Extrastate_War_Participants-1.0.csv")
res = pd.DataFrame(columns=['country','year'])

for i in range(1, len(dataEX)):
    nVeces = (dataEX.at[i,'yrend1'] - dataEX.at[i - 1,'yrbeg1'])
    year = dataEX.at[i - 1,'yrbeg1']
    for j in range(0, nVeces):   
        res = res.append({'country' : dataEX.at[i, 'stateabb'], 'year' : year},ignore_index=True)
        year += 1

dataInter = pd.read_csv("COW_Interstate_War_Participants-1.0.csv")

for i in range(1, len(dataInter)):
    nVeces = (dataInter.at[i,'yrend1'] - dataInter.at[i - 1,'yrbeg1'])
    year = dataInter.at[i - 1,'yrbeg1']
    for j in range(0, nVeces):   
        res = res.append({'country' : dataInter.at[i, 'stateabb'], 'year' : year},ignore_index=True)
        year += 1

dataIntra = pd.read_csv("COW_Intrastate_War_Participants_1.0.csv")

for i in range(1, len(dataInter)):
    nVeces = (dataInter.at[i,'yrend1'] - dataInter.at[i - 1,'yrbeg1'])
    year = dataInter.at[i - 1,'yrbeg1']
    for j in range(0, nVeces):   
        res = res.append({'country' : dataInter.at[i, 'stateabb'], 'year' : year},ignore_index=True)
        year += 1

res.sort_values(by=['country', 'year'], inplace=True)

res.drop_duplicates(subset=['country', 'year'], keep='first', inplace=True)

res.to_csv("WarsPerYearDef.csv",index=False)
