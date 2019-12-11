#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import re
import os
import sys

files = os.listdir(sys.argv[1])
fileNames = []
for file in files:
    if(file.startswith('part')):
        fileNames.append(file)
    
    

#print(data)
data = ["country,year,allies,borderCountries,inversion,gdp,war\n"]

for i in range(0, len(fileNames)):
    part = open(sys.argv[1] + fileNames[i])
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


# In[ ]:




