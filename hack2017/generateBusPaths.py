

# Define a class Route that is a list of X coordinates and list of Y coordinates
# each is a dictionary that maps to 
class Route:
    def __init__(self, routeName):
        self.xlocs = {};
        self.ylocs = {};
        self.locNames = []
        self.routeName = routeName
    
    def __init__(self, routeName, name, x, y):
        self.routeName = routeName
        self.xlocs = {}
        self.ylocs = {}
        self.locNames = []
        self.xlocs[name] =x
        self.ylocs[name] = y
        self.locNames.append(name)
    
    def get(self, numStop):
        return self.locNames[numStop % len(self.locNames)]
        
    def getNextStop(self, nameStop):
        for i in range(0, len(self.routeName)+1):
            #print("hi there")
            #print(self.locNames[i])
            #print(nameStop)
            if (self.locNames[i] == nameStop):
                return self.get(i+1)
        return self.get(0)
    
    def addLoc(self, name, x, y):
        self.xlocs[name] = x
        self.ylocs[name] = y
        self.locNames.append(name)
    
    def getX(self, name):
        return self.xlocs[name]
    
    def getY(self, name):
        return self.ylocs[name]
    
    # Define a toString method to allow for easy visualization
    def __str__(self):
        s = self.routeName + "\n"
        for i in self.locNames :
            s = s + i + ":  (" + str(self.xlocs[i]) + ", " + str(self.ylocs[i]) +")\n"
        return s




def parseX(currStop) :
    beginning = 0
    end = 0
    #print(currStop[0])
    while (beginning < len(currStop) and currStop[beginning] != '-' and (currStop[beginning] > '9' or currStop[beginning] < '0')):
        beginning = beginning + 1
    end = beginning
    while (end < len(currStop) and (currStop[end] == '-' or currStop[end] == '.' or (currStop[end] <= '9' and currStop[end] >= '0'))):
        end = end + 1
#    print(currStop[beginning:-1*(len(currStop) - end)])
    return float(currStop[beginning:-1*(len(currStop) - end)])

def parseY(currStop) :
    beginning = 0
    end = 0
    while(currStop[beginning] != ','):
        beginning = beginning + 1
    while (beginning < len(currStop) and currStop[beginning] != '-' and (currStop[beginning] < '0' or currStop[beginning] > '9')):
        beginning = beginning + 1
    #found beginnning
    #print(beginning)
    #print(currStop[beginning:])
    end = beginning
    
    while (end < len(currStop) and (currStop[end] == '-' or currStop[end] == '.' or (currStop[end] <= '9' and currStop[end] >= '0'))):
        end = end + 1
#    print(currStop[beginning:-1*(len(currStop) - end)])
    return float(currStop[beginning:-1*(len(currStop) - end)])
    

# import files for reading and writing
import pandas as pd
from datetime import datetime, date

# Do not generate warning for changing sheet
pd.options.mode.chained_assignment = None

# Important excel file and set its sheet
xlsx = pd.ExcelFile("busData.xlsx")
sheet1 = xlsx.parse(0) #actually use sheet 2

busRoutes = {}
# iterate row by row through the excel sheet
for i in range(0, len(sheet1)):
    # get the ith row
    row = sheet1.ix[i]
    #print(row)
    if (not row[2] in busRoutes) :
        busRoutes[row[2]] = (Route(row[2], row[1], parseX(row[0]), parseY(row[0])))
    else :
        busRoutes[row[2]].addLoc(row[1], parseX(row[0]), parseY(row[0]))

for i in busRoutes :
    print(i)
    print(busRoutes[i])
    print ("\n\n")

import datetime
from random import *
import math
class Bus:
    BusNumber = 0
    
    def __init__(self, routeName, delta):
        self.busId = Bus.BusNumber
        Bus.BusNumber += 1
        
        self.active = (datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 22)
        
        self.waitTime = delta.seconds
        if (self.waitTime == 0):
            self.waitTime = delta.microSeconds / 1000
        self.route = routeName
        self.prevDest = (busRoutes[routeName]).get(0)
        self.nextDest = (busRoutes[routeName]).get(1)
        self.currX = busRoutes[routeName].getX(self.prevDest)
        self.currY = busRoutes[routeName].getY(self.prevDest)
        self.nextX = busRoutes[routeName].getX(self.nextDest)
        self.nextY = busRoutes[routeName].getY(self.nextDest)
        self.currXDist = self.nextX- self.currX
        self.currYDist = self.nextY - self.currY
        self.waitSteps = 0
        self.stepsTowardsNextDest = 0
        
        self.sincePrevStop = 0
    
    def drive(self, time):
        if time.hour > 5 and time.hour < 22:
            self.active = True
        else:
            self.active = False
        if self.waitSteps > 0:
            self.waitSteps = self.waitSteps - 1
            self.sincePrevStop+=1
            return
        if self.active:
            self.sincePrevStop+=1
            # don't stop here ever
            if random() < .05:
                return

            self.stepsTowardsNextDest+=1
            #print(self.currXDist)
            #print(self.nextX - self.currX)
            #print(self.currYDist)
            #print(self.currY)
            self.currX = self.currX + self.currXDist/(180 / self.waitTime)
            self.currY = self.currY + self.currYDist/(180 / self.waitTime)
            #if it is at the next stop, wait a bit and then start moving to next stop
            if (math.fabs(self.currX - self.nextX)  < 10 ** (-7) and math.fabs(self.currY - self.nextY) < 10 ** (-7)):
                self.waitSteps = uniform((120 / self.waitTime), (240/self.waitTime))
                if (self.nextDest == "Lot 16 & 23"):
                    self.waitSteps = uniform((600 / self.waitTime),(1200 / self.waitTime))
                if (self.nextDest == "Goheen Walk"):
                    self.waitSteps = 0
 
                self.prevDest = self.nextDest
                self.nextDest = busRoutes[self.route].getNextStop(self.prevDest)
                self.nextX = busRoutes[self.route].getX(self.nextDest)
                self.nextY = busRoutes[self.route].getY(self.nextDest)
                self.currXDist= self.nextX - self.currX
                self.currYDist = self.nextY - self.currY
                self.stepsTowardsNextDest = 0
                self.sincePrevStop = 0
        else:
            return
    
    def distanceToNext(self):
        return (self.currX - self.nextX) * (self.currX - self.nextX) + (self.currY - self.nextY) * (self.currY - self.nextY)
    
    def roundDistance(self, dist):
        return int(math.ceil((dist)/self.waitTime)) *self.waitTime
    
    def timeSincePrevStop(self):
        return self.sincePrevStop*self.waitTime
    
    def timeToNextStop(self):
        #print(int(self.waitSteps * self.waitTime))
        #print(self.waitTime*(180/self.waitTime - self.stepsTowardsNextDest))
        return self.roundDistance(int(self.waitSteps * self.waitTime) + int(self.waitTime*(180/self.waitTime - self.stepsTowardsNextDest)))
    
    def getX(self):
        if (self.active):
            return self.currX
        else:
            return 0
    def getY(self):
        if (self.active):
            return self.currY
        else:
            return 0
    
    def getLocation(self):
        return "(" + str(self.getX()) + ", " + str(self.getY()) + ")"
    
    def prevStop(self):
        if (self.active):
            return self.prevDest
        else:
            return "NULL"
    def getNextX(self):
        return self.nextX
    def getNextY(self):
        return self.nextY
    def nextStop(self):
        if (self.active):
            return self.nextDest
        else:
            return "NULL"
    
    def isActive(self):
        return self.active
    
        
    def printLocation(self):
        if(self.active):
            print(str(self.busId) + ": " + self.getLocation())
    
    # Define a toString method to allow for easy visualization
    def __str__(self):
        s = self.route + "\n"
        s = s + "Pos: ( " + str(self.currX) + ", " + str(self.currY) + ")\n"
        s = s + "Past Stop: " + self.prevDest +"\n"
        s = s + "Next Stop: " + self.nextDest
        return s


import numpy as np
    
def writeToDataSheet(currentTime, delta, sheet, numIterations, b1, b2):
    rowNum = 0
    dataframe = {}
    dataframe["Location"] = []
    dataframe["Time"] = []
    dataframe["Bus #"] = []
    dataframe["Prev Dest"] = []
    dataframe["Next Dest"] = []
    dataframe["Time since Prev"] = []
    dataframe["Time to Dest"] = []
    dataframe["Testing"] = []
    dataframe["Distance to Next"] = []
    dataframe["X"] = []
    dataframe["Y"] =[]
    
    for i in range(0, numIterations):
        if (i % (numIterations/10) == 0):
            print("another 10%!")
        b1.drive(currentTime)
        b2.drive(currentTime)
        currentTime = currentTime + delta
        dataframe["Location"].append(b1.getLocation())
        dataframe["Location"].append(b2.getLocation())
        dataframe["Time"].append(currentTime)
        dataframe["Time"].append(currentTime)
        dataframe["Bus #"].append("1")
        dataframe["Bus #"].append("2")
        dataframe["Prev Dest"].append(b1.prevStop())
        dataframe["Prev Dest"].append(b2.prevStop())
        dataframe["Next Dest"].append(b1.nextStop())
        dataframe["Next Dest"].append(b2.nextStop())
        dataframe["Time to Dest"].append(b1.timeToNextStop())
        dataframe["Time to Dest"].append(b2.timeToNextStop())
        dataframe["Time since Prev"].append(b1.timeSincePrevStop())
        dataframe["Time since Prev"].append(b2.timeSincePrevStop())
        dataframe["Distance to Next"].append(b1.distanceToNext())
        dataframe["Distance to Next"].append(b2.distanceToNext())
        dataframe["X"].append(b1.getX())
        dataframe["X"].append(b2.getX())
        dataframe["Y"].append(b1.getY())
        dataframe["Y"].append(b2.getY())
        #rowNum = rowNum+2
    dataframe["Testing"] = np.random.uniform(0, 1, 2*numIterations) <= .75
    return dataframe
'''
from datetime import timedelta
delta = timedelta(seconds = 10)
currentTime = datetime.datetime.now()
#print(currentTime)
#currentTime = currentTime + delta
print(currentTime)
b1 = Bus("Central", delta)
b2 = Bus("E-Quad", delta)

print(b1.roundDistance(143.23452))
'''
#sheet1 = xlsx.parse(1) #actually use sheet 2
#start bus1 at Goheen Walk
#start bus2 at Equad
# every one 10 seconds data seta
from datetime import timedelta
delta = timedelta(seconds = 10)
currentTime = datetime.datetime.now()
#print(currentTime)
#currentTime = currentTime + delta
print(currentTime)
b1 = Bus("Central", delta)
b2 = Bus("E-Quad", delta)

'''
for i in range(1, 1000):
    b2.drive(currentTime)
    b2.printLocation()
    print(b2.distanceToNext())

'''
sheet1 = writeToDataSheet(currentTime, delta, sheet1, 100000, b1, b2)
df = pd.DataFrame(sheet1)
writer = pd.ExcelWriter('sampledata10.xlsx', engine = 'xlsxwriter', datetime_format='hh:mm:ss')
df.to_excel(writer, 'Sample Data', index = False)
# ESTABLISH WRITER TO WRITE TO OUTPUT FILE

df.to_excel(writer, 'Sample Data', index = False)
#sheet1.to_excel(writer, 'Sample Data', index = False)
sheet = writer.book.worksheets()[0]
print("done with seconds10")
# Center the worksheet
#sheet1['DATE'] = pd.to_datetime(sheet1['Time']).dt.strftime('%-m/%-d/%y')
center = writer.book.add_format({'align': 'center'})
sheet.set_column('A:G', None, center)

# Following column widths are arbitrary that look good
# sets the width of the first column to 8
sheet.set_column(0, 0, 10)
sheet.set_column(1, 1, 35)
# sets width of remaining columns to 13
sheet.set_column(2, 3, 25)
sheet.set_column(4,4, 15)


# save the file
writer.save()
