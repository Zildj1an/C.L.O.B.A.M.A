#!/usr/bin/env python
# coding: utf-8


##########################################
# ALGORITHM  FOR CLOUD AND BIG DATA      #
# Authors: Carlos Bilbao, Álvaro Ortiz   #
##########################################


#Need to -> pip install scikit-plot
import scikitplot as skplt
import pandas as pd
import numpy as np
import sklearn.metrics
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

############################
# 1 PREPARATION		       #
############################

ddbb_wars = pd.read_csv("result.csv", na_values='')

# Feature names
headers_wars = list(ddbb_wars)


############################
# 2 DATA EXPLORATION       #
############################

# Column names
print("Wars Features:")
print(headers_wars,'\n')
print("Columns in Wars = ", len(headers_wars))

# Unique elements of column Country
countries = set(ddbb_wars["country"])
print("Unique elems in column Country for wars = ", countries)


############################
# 3 PREPROCESSING          #
############################

# Feature matrix
X = []

# Label Array
y = []

# We prepare the matrix with the data
for index, row in ddbb_wars.iterrows():

	vector = [#le.transform([row['country']])[0],
              #row['year'],
			  row['inversion'],
			  row['gdp']]
	X.append(vector)
	y.append(row['war'])

X = np.asarray(X)

#X = preprocessing.normalize(X, norm='l2')


############################
# 4 CLASSIFICATION         #
############################

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

clf = LogisticRegression(random_state=0, solver="lbfgs").fit(X_train, y_train)

probs = clf.predict_proba(X_train[:1, :])
score = clf.score(X_test, y_test)
y_pred = clf.predict(X)


############################
# 5 CONFUSION MATRIX       #
############################
skplt.metrics.plot_confusion_matrix(y, y_pred, normalize=True)



############################
# 6 INTERESTING DATA       #
############################

start = time.time()

#Plots the data
for i in range(0, X[:, 0].size):
    color = 'b'
    marker = 'o'
    
    if(y[i] == True): # -> WAR
        color = 'r'
        marker = 'x'
        
    plt.plot(X[i, 1], X[i, 0], marker, c = color)
    
plt.xlabel('GDP')
plt.ylabel('Militar Inversion')
fig = plt.gcf()
fig.set_size_inches(10, 10)

finished = time.time()
elapse = finished - start

plt.show()

print("Time(ms): " + str(elapse))

