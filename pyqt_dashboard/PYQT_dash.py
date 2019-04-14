#!/usr/bin/env python

from PyQt5 import QtWidgets, QtGui
import pyqtgraph as pg
from TimeGraph import TimeGraph, DataModuleManager
from Layouts import *
from WebsocketProcess import WebsocketProcess


# Graph manager needs to be able to recieve data
# from seperate threads to update all graphs

def main():
    app = QtWidgets.QApplication([])

    dmm = DataModuleManager()
    # Initalize main window widget
    window = QtGui.QWidget()

    pg.setConfigOptions(antialias=False)

    # Initalize main layout and
    tabs = QtWidgets.QTabWidget()
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(tabs)
    window.setLayout(layout)

    # Add layouts to window
    cl = CriticalLayout(dmm)
    tabs.addTab(cl, "Critical")

    dl = DynamicsLayout(dmm)
    tabs.addTab(dl, "Dynamics")

    ct = CANTableLayout(dmm)
    tabs.addTab(ct, "CAN Table")

    # Display window
    window.show()
    window.resize(1600, 600)
    window.raise_()

    wsp = WebsocketProcess(dmm)
    wsp.start()

    app.exec_()


if __name__ == "__main__":
    main()
