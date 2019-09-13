#!/usr/bin/env python

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QInputDialog, \
    QApplication

import pyqtgraph as pg
from DataReadouts import TimeGraph, DataModuleManager
from Layouts import CriticalLayout, DynamicsLayout, TuningLayout, \
    CANTableLayout

from WebsocketProcess import *
import sys


# Graph manager needs to be able to recieve data
# from seperate threads to update all graphs

DEFAULT_WS_ADDRESS = "ws://192.168.4.1:5000"
# DEFAULT_WS_ADDRESS = "ws://127.0.0.1:5000"


def main():
    app = QApplication([])

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook

    dmm = DataModuleManager()
    # Initalize main window widget
    window = QWidget()

    pg.setConfigOptions(antialias=False, useOpenGL=True)

    # Initalize main layout and
    tabs = QTabWidget()
    layout = QVBoxLayout()
    layout.addWidget(tabs)
    window.setLayout(layout)

    # Add layouts to window
    cl = CriticalLayout(dmm)
    tabs.addTab(cl, "Critical")

    dl = DynamicsLayout(dmm)
    tabs.addTab(dl, "Dynamics")

    tl = TuningLayout(dmm)
    tabs.addTab(tl, "Tuning Layout")

    ct = CANTableLayout(dmm)
    tabs.addTab(ct, "CAN Table")

    # Display window
    window.show()
    window.resize(1600, 600)
    window.raise_()

    result, address = getWebsocketAddress(window)

    if result:
        wsp = WebsocketProcess(dmm, address, isDebug=False)
        wsp.start()
    else:
        sys.exit()

    app.exec_()


def getWebsocketAddress(window):
    result = False
    address = DEFAULT_WS_ADDRESS

    while not result:
        address, result = QInputDialog.getText(window, 'Disconnected',
                                               'Enter WS address',
                                               text=DEFAULT_WS_ADDRESS)
    return (result, address)


if __name__ == "__main__":
    main()
