import pandas as pd
import re
import os

files = os.listdir()
fileNames = []
for file in files:
    if(file.startswith('part')):
        fileNames.append(file)
    
    

#print(data)
data = ["country,year,allies,borderCountries,inversion,gdp,war\n"]

for i in range(0, len(fileNames)):
    part = open(fileNames[i])
    data.append(part.read()
          .replace("'", "")
          .replace('(', "")
          .replace(')', "")
          .replace(' ', "")
          .replace("\"\"", "")
        )
        
f = open("result.csv","w+")
for line in data:
    f.write(line)

f.close()