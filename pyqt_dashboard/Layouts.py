from PyQt5 import QtWidgets, QtGui
from TimeGraph import TimeGraph

# Master class for all readout layouts
# Contains methods for easily adding data readouts
# in multiple contexts
class ReadoutLayout(QtGui.QWidget):
    def __init__(self, moduleManager , parent=None):
        super().__init__(parent=parent)
        self.masterLayout = QtGui.QGridLayout()
        self.setLayout(self.masterLayout)
        self.moduleManager = moduleManager
    
    # Create new graph and add to handler
    def createGraph(self, title):
        newGraph = None
        if self.moduleManager:
            newGraph = TimeGraph(title)
            self.moduleManager.manageModule(newGraph)
        return newGraph

    # Create and place new graph in a specific location
    def placeNewGraph(self, title, position):
        newGraph = self.createGraph(title)
        self.masterLayout.addWidget(newGraph.getWidget(), *position)
        return newGraph
    
    # TODO Create more readout modules to add to layouts


class CriticalLayout(ReadoutLayout):
    def __init__(self, moduleManager, parent=None):
        super().__init__(moduleManager, parent=parent)

        self.placeNewGraph("Batery Temp", (1,1))
        

class DynamicsLayout(ReadoutLayout):
    def __init__(self,moduleManager, parent=None):
        super().__init__(moduleManager, parent=parent)

        self.placeNewGraph("Speed", (1,1))
        self.placeNewGraph("Air Temp", (1,2))
