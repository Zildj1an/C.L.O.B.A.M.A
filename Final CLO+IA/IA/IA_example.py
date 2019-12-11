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
from sklearn.svm import LinearSVC



############################
# 1 PREPARATION		       #
############################
start = time.time()

ddbb_wars = pd.read_csv("result.csv", na_values='')

# Feature names
headers_wars = list(ddbb_wars)



############################
# 2 PREPROCESSING          #
############################

# Feature matrix
X = []

# Label Array
y = []

# We prepare the matrix with the data
for index, row in ddbb_wars.iterrows():

    vector = [row['inversion'], row['gdp']]
    X.append(vector)
    y.append(row['war'])

X = np.asarray(X)

finished = time.time()
elapse = finished - start
print("Time to get data: " + str(elapse) + " seconds")
print()



############################
# 3 DATA EXPLORATION       #
############################

# Column names
print("Wars Features:")
print(headers_wars,'\n')
print("Columns in Wars = ", len(headers_wars))


# Unique elements of column Country
countries = set(ddbb_wars["country"])
print("Acronyms of Countries: ", countries)



############################
# 3.1 PLOTTING DATA        #
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

plt.show()

finished = time.time()
elapse = finished - start
print("Time(s): " + str(elapse))



############################
# 4 CLASSIFICATION         #
############################

start = time.time()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 0)

# (1) Create the model and fit
clf = GaussianNB().fit(X_train, y_train)

# (2) Predict
y_pred = clf.predict(X_test)


finished = time.time()
elapse = finished - start
print("Time(s) to train GaussianNB AI: " + str(elapse) + " seconds")
print()




############################
# 4.1 CONFUSION MATRIX     #
############################

print("Accuracy:" + str(int(np.round(sklearn.metrics.accuracy_score(y_test, y_pred), 2) * 100)) + "%")
skplt.metrics.plot_confusion_matrix(y_test, y_pred, normalize=True)




############################
# 5 OTHER IMPLEMENTATIONS  #
############################

start = time.time()

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

# (1) Create the model
SVCclf = LinearSVC(max_iter=10000) #You can change the iterations

# (2) Fit the model
SVCclf.fit(x_train, y_train)

# (3) Predict
y_pred = SVCclf.predict(x_test)

finished = time.time()
elapse = finished - start
print("Time(s): " + str(elapse))
print()



############################
# 5.1 CONFUSION MATRIX     #
############################

print("Accuracy:" + str(int(np.round(sklearn.metrics.accuracy_score(y_test, y_pred), 2) * 100)) + "%") #Thats the reason that we plot the Confusion Matrix
skplt.metrics.plot_confusion_matrix(y_test, y_pred, normalize=True) # you can see that the AI is always predicting 'NO WAR' result -> 63% Accuracy (sure?)

