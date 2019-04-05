import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
import time
import random
import numpy as np
import pandas as pd
import datetime

def timestamp():
    return time.time()

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S") for value in values]

class TimeGraph():
    def __init__(self, title):
        # self.mainLayout = QtWidgets.QVBoxLayout()
        # self.setLayout(self.mainLayout)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100) # in milliseconds
        self.timer.timeout.connect(self.onTimerPulse)
        self.timer.start()

        self.plotItem = pg.PlotWidget(title=title, axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        self.plotDataItem = self.plotItem.plot([], pen='r' , 
            symbolBrush=(255,0,0), symbolSize=5, symbolPen=None)

        self.xVals = []
        self.yVals = []
        self.maxPoints = 100
        self.title = title

    def updateGraph(self):
        self.plotDataItem.setData(self.xVals, self.yVals)

    def addDataPoint(self, x, y):
        self.xVals.extend(x)
        self.yVals.extend(y)

        self.xVals = self.xVals[-self.maxPoints:]
        self.yVals = self.yVals[-self.maxPoints:]

        self.updateGraph()
    
    def setData(self, newXVals, newYVals):
        self.xVals = newXVals[-self.maxPoints:]
        self.yVals = newYVals[-self.maxPoints:]

    def onTimerPulse(self):
        x = [timestamp()]
        y = [random.random()]
        self.addDataPoint(x, y)

    def getWidget(self):
        return self.plotItem

class GraphManager():

    def __init__(self):
        self.allGraphs = []

    def manageGraph(self, newGraph):
        self.allGraphs.append(newGraph)

    # Called whenever new data is to be pushed to 
    # any graph which is being displayed
    def onDataCallback(self, name, value):

        for g in self.allGraphs:
            if g.title == name:
                g.addDataPoint(data, timestamp())
                return