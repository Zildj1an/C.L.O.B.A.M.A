#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8



#Need to -> pip install scikit-plot
import scikitplot as skplt

#Need to -> pip install pandas
import pandas as pd
import numpy as np
import sklearn.metrics
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


############################
# 1 PREPARATION            #
############################
start = time.time()

ddbb_wars = pd.read_csv("result.csv", na_values='')

actualYear = 2019; #If result.csv is updated, change this

# Feature names
headers_wars = list(ddbb_wars)


############################
# 2 PREPROCESSING          #
############################

# Feature matrix
X = []

# Label Array
y = []

dataOfCountries = [] #Data we are not going to train


XActualYear = [] #Get the last data of the countries
#YActualYear = [] #Get the last data of the countries

# We prepare the matrix with the data
for index, row in ddbb_wars.iterrows():
    vector = [row['inversion'], row['gdp']]
    
    if(row['year'] == actualYear):
        XActualYear.append(vector)
        borderCountries = np.asarray(row['borderCountries'].split(','))
        dataOfCountries.append([row['country'], borderCountries])
        #YActualYear.append(row['war']) #Dont needed
    else:
        X.append(vector)
        y.append(row['war'])

X = np.asarray(X) #data to numpy array
XActualYear = np.asarray(XActualYear)


finished = time.time()
elapse = finished - start
print("Time to get data: " + str(elapse) + " seconds")
print()



############################
# 3 CLASSIFICATION         #
############################

start = time.time()

clf = GaussianNB().fit(X, y) #Trained X, we dont need to split the data
    # because we want to classify XActualYear

yActualYear_pred = clf.predict(XActualYear)

finished = time.time()
elapse = finished - start
print("Time(s) to train GaussianNB AI: " + str(elapse) + " seconds")
print()


############################
# 4 PLOTTING DATA          #
############################
#Plots the data for the Actual Year
for i in range(0, len(XActualYear)):
    color = 'b'
    marker = 'o'
    
    if(yActualYear_pred[i]): # -> WAR
        color = 'r'
        marker = 'x'
        
    plt.plot(XActualYear[i, 1], XActualYear[i, 0], marker, c = color)

plt.title('Year ' + str(actualYear))
plt.xlabel('GDP')
plt.ylabel('Militar Inversion')
fig = plt.gcf()
fig.set_size_inches(10, 10)

finished = time.time()
elapse = finished - start

plt.show()

print("Time to plot the data: " + str(elapse) + " seconds")


############################
# 4 PRINT COUNTRIES        #
############################

boolMatrix = np.zeros(len(yActualYear_pred)) #Boolean matrix
nWars = 0

for i in range(0, len(yActualYear_pred)):
    
    if(yActualYear_pred[i] == True): #War
        if(boolMatrix[i] == False):
            nWars += 1 #One more war
            print(str(nWars) + ". \t" + dataOfCountries[i][0] + ":") #Country

            
            for j in range(0, len(dataOfCountries[i][1])): #Colindants
                                
                for k in range(j + 1, len(yActualYear_pred)): #Search Colindants
                    
                    if(not boolMatrix[k] #Not marked
                       and dataOfCountries[i][1][j] == dataOfCountries[k][0] #Coincident
                       and yActualYear_pred[k]): #Colindant war
                        print("\t" + dataOfCountries[k][0])
                        boolMatrix[k] = True;
    
    boolMatrix[i] = True;
            



