# I need routes for dummy real time GPS
# once actual real time GPS, don't need the routes in this class
# just read from real time GPS

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
        for i in range(0, len(self.routeName)):
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
    
# EVERYTHING ABOVE, WILL BE GOOOONE!

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

# EVERYTHING ABOVE WILL BE GONE, DONT NEED TO READ THE BUS ROUTES

import datetime
from random import *

class Bus:
    BusNumber = 0
    
    def __init__(self, routeName):
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
        self.waitSteps = 0
    
    def drive(self, time):
        if time.hour > 5 and time.hour < 22:
            self.active = True
        else:
            self.active = False
        if self.waitSteps > 0:
            self.waitSteps = self.waitSteps - 1
            return
        if self.active:
            # don't stop here ever
            if random() < .05:
                return
            
            self.currX = self.currX + (self.nextX - self.currX)/(180 / self.waitTime)
            self.currY = self.currY + (self.nextY - self.currY)/(180 / self.waitTime)
            #if it is at the next stop, wait a bit and then start moving to next stop
            if (self.currX - self.nextX  < 10 ** (-12) and self.currY - self.nextY < 10 ** (-12)):
                self.waitSteps = uniform((120 / self.waitTime), (240/self.waitTime))
                if (self.nextDest == "Lot 16 & 23"):
                    self.waitSteps = uniform((600 / self.waitTime),(1200 /self.waitTime))
                if (self.nextDest == "Goheen Walk"):
                    self.waitSteps = 0
                self.prevDest = self.nextDest
                self.nextDest = busRoutes[self.route].getNextStop(self.prevDest)
        else:
            return
        
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



# REAL TIME DATA (FAKED)
#start bus1 at Goheen Walk
#start bus2 at Equad
from datetime import timedelta
delta = timedelta(seconds = 10)
currentTime = datetime.datetime.now()
#print(currentTime)
#currentTime = currentTime + delta
print(currentTime)
b1 = Bus("Central")
b2 = Bus("E-Quad")
import time
delta = timedelta(microseconds = 100)


while (1) :
    time.sleep(delta.microseconds/1000)
    b1.drive(datetime.datetime.now())
    b2.drive(datetime.datetime.now())
    b1.printLocation()
    b2.printLocation()

    #currentTime = currentTime + delta