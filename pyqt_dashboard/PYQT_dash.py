#!/usr/bin/env python

from PyQt5 import QtWidgets, QtGui
import pyqtgraph as pg
from TimeGraph import TimeGraph, GraphManager
from Layouts import CriticalLayout, DynamicsLayout

def main():
    app = QtWidgets.QApplication([])
    
    # Initalize main window widget
    window = QtGui.QWidget()

    pg.setConfigOptions(antialias=True)

    # Initalize main layout and
    tabs = QtWidgets.QTabWidget()
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(tabs)
    window.setLayout(layout)

    gm = GraphManager()

    # Add layouts to window
    cl = CriticalLayout(graphHandle=gm)
    tabs.addTab(cl,"Critical")

    dl = DynamicsLayout()
    tabs.addTab(dl,"Dynamics")

    window.show()
    window.resize(1600,600) 
    window.raise_()
    app.exec_()    
    
if __name__ == "__main__":
    main()