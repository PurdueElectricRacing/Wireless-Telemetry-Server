from PyQt5 import QtWidgets, QtGui

class ReadoutLayout(QtGui.QWidget):
    def __init__(self, graphHandle = None, parent=None):
        super().__init__(parent)
        self.masterLayout = QtGui.QGridLayout()
        self.setLayout(self.masterLayout)
        self.graphHandle = graphHandle
    
    def createGraph(self, title):
        newGraph = None
        if self.graphHandle:
            newGraph = TimeGraph(title)
            self.graphHandle.manageGraph(newGraph)
        return newGraph



class CriticalLayout(ReadoutLayout):
    def __init__(self, graphHandle, parent=None):
        super().__init__(graphHandle=graphHandle, parent=parent)
        
        g = self.createGraph("Adam")

        self.masterLayout.addWidget(g.getWidget(), 1,1)


class DynamicsLayout(ReadoutLayout):
    def __init__(self, parent=None):
        super().__init__(parent)