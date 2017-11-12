# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier

# Load pandas
import pandas as pd

# Load numpy
import numpy as np

# Set random seed
np.random.seed(0)

# Do not generate warning for changing sheet
pd.options.mode.chained_assignment = None

# Important excel file and set its sheet
xlsx = pd.ExcelFile("sampledata10.xlsx")
df = xlsx.parse(0) #actually use sheet 2
#print(sheet1)
#print(df.head())
#print(df.columns)
stopsFactored = pd.factorize(df["Prev Dest"])
df["Stop Numbers"] = stopsFactored[0]

# Create two new dataframes, one with the training rows, one with the test rows
train, test = df[df['Testing']==True], df[df['Testing']==False]

#Create a list of the feature column's names
features =[]
features.append("X")
features.append("Y")
features.append("Distance to Next")
features.append("Time since Prev")
features.append("Stop Numbers")

#features.append("Prev Dest")



clf = RandomForestClassifier(n_jobs=2, random_state = 0)
clf.fit(train[features], train["Time to Dest"])
clf.predict(test[features])
preds = clf.predict(test[features])
sumDiffs = 0


mat = test.as_matrix(columns=test.columns[8:-3])
arr = np.squeeze(np.asarray(mat))
#print(arr)
#print(arr)
import math
for i in range(0, len(test)):
    sumDiffs += math.fabs(preds[i] - arr[i])

#print(sumDiffs/len(test))

def getTimePrediction(x,y,distNext, tPrev, stop):
    rtArr = []
    rtArr.append(x)
    rtArr.append(y)
    rtArr.append(distNext)
    rtArr.append(tPrev)
    
    for i in range(0, len(stopsFactored)):
        if(stopsFactored[i] == stop):
            rtArr.append(i)
            return clf.predict(rtArr)
    rtArr.append(0)
    return clf.predict(rtArr)

from bus import Route
from bus import getRoutes
busRoutes = getRoutes()
'''
for i in busRoutes:
    print(str(i))
    print(str(busRoutes[i]))
#print(str(busRoutes))
'''
MAXTIME = 10**12

#first arg is name of the stop

import sys
'''
def predict(stop):
    for i in busRoutes:
        if stop in i:
            time = predict(i, stop)
            if time < MAXTIME:
                MAXTIME = time
    return MAXTIME
'''
from generateBusPaths import getAllTimePredictions

'''
[{"bus": "0", "pos":{"lat":40.346973900000044,"lng":-74.65898150000007}, "rt":"Central", "prevDest":"Dod Hall", "distNext":7.111672198820459e-07, "tPrev":40},
{"bus": "1", "pos":{"lat":40.34649970000003,"lng":-74.65418439999989}, "rt":"E-Quad", "prevDest":"Frist/Guyot (Southbound)", "distNext":6.1249782497886385e-06, "tPrev":40}]
'''

def predict():
    MAXTIME = 10**12
    desiredStop = sys.argv[0]
    timesAtEachStop = {}
    
    for i in busRoutes:
        timesAtEachStop[i] = MAXTIME
    i = 0
    while ((len(sys.argv) - i) / 5 > 0):
        i += 1
        locX = sys.argv[i]
        i+= 1
        LocY = sys.argv[i]
        i += 1
        route = sys.argv[i]
        i += 1
        stop = sys.argv[i]
        i += 1
        distNext = float(sys.argv[i])
        i +=1 
        tPrev = float(sys.argv[i])
        tempTimes = getAllTimePredictions(getTimePrediction(locX, locY, distNext, tPrev, stop), route, stop)
        for j in tempTimes:
            if tempTimes[j] < timesAtEachStop[j]:
                timesAtEachStop[j] = tempTimes[j]
        
    return timesAtEachStop[desiredStop]
    
#generateBusPaths.getTimes(time, routeName, prevStop)
