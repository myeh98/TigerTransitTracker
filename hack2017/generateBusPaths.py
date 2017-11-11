

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
    
from random import *

class Bus:
    def __init__(self, routeName):
        self.route = routeName
        self.prevDest = (busRoutes[routeName]).get(0)
        self.nextDest = (busRoutes[routeName]).get(1)
        self.currX = busRoutes[routeName].getX(self.prevDest)
        self.currY = busRoutes[routeName].getY(self.prevDest)
        self.nextX = busRoutes[routeName].getX(self.nextDest)
        self.nextY = busRoutes[routeName].getY(self.nextDest)
        self.waitSteps = 0
    
    def drive(self, time):
        if self.waitSteps > 0:
            self.waitSteps = self.waitSteps - 1
            return
        if time.hour > 5 and time.hour < 22:
            # don't stop here ever
            if self.prevDest == "Goheen Walk":
                5 -4 # dumb command just to allow for indentation
            # higher chance of stopping at this stop
            elif self.prevDest == "Lot 16 & 23" and random() < .3:
                return
            elif random() < .05:
                return
            
            self.currX = self.currX + (self.nextX - self.currX)/10
            self.currY = self.currY + (self.nextY - self.currY)/10
            #if it is at the next stop, wait a bit and then start moving to next stop
            if (self.currX - self.nextX  < 10 ** (-12) and self.currY - self.nextY < 10 ** (-12)):
                self.waitSteps = 20
                if (self.nextDest == "Lot 16 & 23"):
                    self.waitSteps = 200
                self.prevDest = self.nextDest
                self.nextDest = busRoutes[self.route].getNextStop(self.prevDest)
        
    def getX(self):
        return self.currX
    def getY(self):
        return self.currY
    
    def getLocation(self):
        return "(" + str(self.getX()) + ", " + str(self.getY()) + ")"
    
    def prevStop(self):
        return self.prevDest
        
    def nextStop(self):
        return self.nextDest
            
    # Define a toString method to allow for easy visualization
    def __str__(self):
        s = self.route + "\n"
        s = s + "Pos: ( " + str(self.currX) + ", " + str(self.currY) + ")\n"
        s = s + "Past Stop: " + self.prevDest +"\n"
        s = s + "Next Stop: " + self.nextDest
        return s



    
def writeToDataSheet(currentTime, delta, sheet, numIterations, b1, b2):
    rowNum = 0
    for i in range(0, numIterations):
        b1.drive(currentTime)
        b2.drive(currentTime)
        currentTime = currentTime + delta
        sheet["Location"][rowNum]  = b1.getLocation()
        sheet["Time"][rowNum] = currentTime
        sheet["Bus #"][rowNum] = "1"
        sheet["Prev Dest"][rowNum] = b1.prevStop()
        sheet["Next Dest"][rowNum] = b1.nextStop()
        sheet["Location"][rowNum+1] = b2.getLocation()
        sheet["Time"][rowNum+1] = currentTime
        sheet["Bus #"][rowNum+1] = "2"
        sheet["Prev Dest"][rowNum+1] = b2.prevStop()
        sheet["Next Dest"][rowNum+1] = b2.nextStop()
        rowNum = rowNum + 2
    return sheet

sheet1 = xlsx.parse(1) #actually use sheet 2
#start bus1 at Goheen Walk
#start bus2 at Equad
# every one 10 seconds data seta
import datetime
from datetime import timedelta
delta = timedelta(seconds = 10)
currentTime = datetime.datetime.now()
#print(currentTime)
#currentTime = currentTime + delta
print(currentTime)
b1 = Bus("Central")
b2 = Bus("E-Quad")
sheet1 = writeToDataSheet(currentTime, delta, sheet1, 10000000, b1, b2)
        

# ESTABLISH WRITER TO WRITE TO OUTPUT FILE
writer = pd.ExcelWriter('sampledata10.xlsx', engine = 'xlsxwriter')
sheet1.to_excel(writer, 'Sample Data', index = False)
sheet = writer.book.worksheets()[0]
print("done with seconds10")
# Center the worksheet
center = writer.book.add_format({'align': 'center'})
sheet.set_column('A:G', None, center)

# Following column widths are arbitrary that look good
# sets the width of the first column to 8
sheet.set_column(0, 0, 30)
sheet.set_column(1, 1, 20)
# sets width of remaining columns to 13
sheet.set_column(2, 2, 13)
sheet.set_column(3,4, 30)


# save the file
writer.save()



# every 5 seconds data set
delta = timedelta(seconds = 5)
b1 = Bus("Central")
b2 = Bus("E-Quad")
sheet1 = writeToDataSheet(currentTime, delta, sheet1, 200000000, b1, b2)
print("done with seconds5")    


# ESTABLISH WRITER TO WRITE TO OUTPUT FILE
writer = pd.ExcelWriter('sampledata5.xlsx', engine = 'xlsxwriter')
sheet1.to_excel(writer, 'Sample Data', index = False)
sheet = writer.book.worksheets()[0]

# Center the worksheet
center = writer.book.add_format({'align': 'center'})
sheet.set_column('A:G', None, center)

# Following column widths are arbitrary that look good
# sets the width of the first column to 8
# sets the width of the first column to 8
sheet.set_column(0, 0, 30)
sheet.set_column(1, 1, 20)
# sets width of remaining columns to 13
sheet.set_column(2, 2, 13)
sheet.set_column(3,4, 30)


# save the file
writer.save()

# every 1 second data set
delta = timedelta(seconds = 1)
sheet1 = writeToDataSheet(currentTime, delta, sheet1, 100000000, b1, b2)
print("done with seconds1")

# ESTABLISH WRITER TO WRITE TO OUTPUT FILE
writer = pd.ExcelWriter('sampledata1.xlsx', engine = 'xlsxwriter')
sheet1.to_excel(writer, 'Sample Data', index = False)
sheet = writer.book.worksheets()[0]

# Center the worksheet
center = writer.book.add_format({'align': 'center'})
sheet.set_column('A:G', None, center)

# Following column widths are arbitrary that look good
# sets the width of the first column to 8
# sets the width of the first column to 8
sheet.set_column(0, 0, 30)
sheet.set_column(1, 1, 20)
# sets width of remaining columns to 13
sheet.set_column(2, 2, 13)
sheet.set_column(3,4, 30)


# save the file
writer.save()


'''    
    # do not perform calculations on the header row
    if (row[2] == 'BUY'):
        # calculate how much profit from buying
        x = buy(row[3], float(row[5]), float(row[4]))
        #print("Profit: %s" %x)
        # if no profit do not add anything to sheet
        if (x != float('nan')):
            # else add to data sheet
            sheet1["REALIZED P&L"][i] = x
    # if not buying a stock, must be selling/shorting
    else:
        # calculate profit from selling/shorting
        x = sell(row[3], float(row[5]), float(row[4]))
        # if no profit do not add anything to sheet
        if (x != float('nan')):
            # else add to data sheet
            sheet1["REALIZED P&L"][i]  = x

# format the dates similar to how they were presented
sheet1['DATE'] = pd.to_datetime(sheet1['DATE']).dt.strftime('%-m/%-d/%y')

# ESTABLISH WRITER TO WRITE TO OUTPUT FILE
writer = pd.ExcelWriter('sampledataOutput.xlsx', engine = 'xlsxwriter')
sheet1.to_excel(writer, 'Sample Data', index = False)
sheet = writer.book.worksheets()[0]

# Center the worksheet
center = writer.book.add_format({'align': 'center'})
sheet.set_column('A:G', None, center)

# Following column widths are arbitrary that look good
# sets the width of the first column to 8
sheet.set_column(0, 0, 8)
# sets the width of the second column to 30
sheet.set_column(1, 1, 30)
# sets width of remaining columns to 13
sheet.set_column(2, 6, 13)

# save the file
writer.save()
'''