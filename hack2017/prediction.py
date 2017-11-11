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
print(df.head())
print(df.columns)
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
print(arr)
#print(arr)
import math
for i in range(0, len(test)):
    sumDiffs += math.fabs(preds[i] - arr[i])

print(sumDiffs/len(test))

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

