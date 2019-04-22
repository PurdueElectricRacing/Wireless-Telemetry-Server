from PyQt5.QtGui import QWidget, QGridLayout, QLineEdit

from PyQt5.QtGui import QHBoxLayout, QPushButton
from DataReadouts import *
import pyqtgraph as pg


# Master class for all readout layouts
# Contains methods for easily adding data readouts
# in multiple contexts
class ReadoutLayout(QWidget):
    def __init__(self, moduleManager, parent=None):
        super().__init__(parent=parent)
        self.masterLayout = QGridLayout()
        self.setLayout(self.masterLayout)
        self.moduleManager = moduleManager

    # Create and place new graph in a specific location
    def placeNewGraph(self, title, dataSpec,  position, data_range=(0, 5000)):
        newGraph = TimeGraph(title, dataSpec, data_range)
        self.moduleManager.manageModule(newGraph)
        self.masterLayout.addWidget(newGraph.getWidget(), *position)
        return newGraph

    def placeText(self, title, spec, position):
        newText = RawText(title, spec)
        self.moduleManager.manageModule(newText)
        self.masterLayout.addWidget(newText.getWidget(), *position)
        return newText

    def placeCANTable(self):
        table = CANTable()
        self.moduleManager.manageModule(table)
        self.masterLayout.addWidget(table.getWidget(), 2, 1)
        return table

    def placeCANSender(self):
        id_field = QLineEdit()
        id_field.setFixedWidth(100)
        id_field.setPlaceholderText("CAN ID")

        message_field = QLineEdit()
        message_field.setFixedWidth(300)
        message_field.setPlaceholderText("Message")

        send_button = QPushButton("Send")
        send_button.setFixedWidth(80)

        def sendMessage():
            print(id_field.text())
            pass

        send_button.clicked.connect(sendMessage)

        layout = QHBoxLayout()
        layout.addWidget(id_field)
        layout.addWidget(message_field)
        layout.addWidget(send_button)
        layout.addStretch()

        self.masterLayout.addLayout(layout, 1, 1)

    def placeLightArray(self, specs, position):
        lights = LightArray(specs)
        self.moduleManager.manageModule(lights)
        self.masterLayout.addLayout(lights.getWidget(), *position)


class CriticalLayout(ReadoutLayout):
    def __init__(self, moduleManager, parent=None):
        super().__init__(moduleManager, parent=parent)

        SDC = [
            DataSpec('501', 'IMD', 'throttle_1'),
            DataSpec('501', 'BMS', 'brake_1'),
            DataSpec('501', 'BSPD', 'brake_1'),
            DataSpec('501', 'INRT', 'brake_1'),
            DataSpec('501', 'Front', 'brake_1'),
            DataSpec('501', 'Main', 'brake_1'),
            DataSpec('501', 'Right', 'brake_1'),
            DataSpec('501', 'Left', 'brake_1'),
            DataSpec('501', 'HVD', 'brake_1'),
            DataSpec('501', 'TSMS', 'brake_1')
            ]
        self.placeLightArray(SDC, (1, 1))

        throttleLine = [DataSpec('501', 'timestamp', 'throttle_1')]
        self.placeNewGraph("Throttle 1", throttleLine, (1, 2))
        throttleLine = [DataSpec('501', 'timestamp', 'throttle_2')]
        self.placeNewGraph("Throttle 2", throttleLine, (2, 1, 1, 2))


class TuningLayout(ReadoutLayout):
    def __init__(self, moduleManager, parent=None):
        super().__init__(moduleManager, parent=parent)

        torque = [
            DataSpec('0AC', 'timestamp', 'cmd_torque'),
            DataSpec('0AC', 'timestamp', 'fdbk_torque', line_color='w'),
            DataSpec('0A5', 'timestamp', 'speed', line_color='g')
            ]
        self.placeNewGraph("Torque Command", torque, (1, 1, 1, 2),
                           data_range=(0, 150000 / 2))

        iDGraph = [
            DataSpec('0AD', 'timestamp', 'id_cmd'), 
            DataSpec('0A8', 'timestamp', 'id_fdbk', line_color='w')
            ]
        self.placeNewGraph("ID Command", iDGraph, (2, 1), data_range=(0, 30))

        iQGraph = [
            DataSpec('0AD', 'timestamp', 'iq_cmd'),
            DataSpec('0A8', 'timestamp', 'iq_fdbk', line_color='w')
            ]
        self.placeNewGraph("IQ Command", iQGraph, (2, 2), data_range=(0, 30))


class DynamicsLayout(ReadoutLayout):
    def __init__(self, moduleManager, parent=None):
        super().__init__(moduleManager, parent=parent)

        brakeLine = [
            DataSpec('501', 'timestamp', 'brake_1'),
            DataSpec('501', 'timestamp', 'brake_2', line_color='w')
            ]
        self.placeNewGraph("Brake", brakeLine, (1, 1))

        throttleLine = [
            DataSpec('501', 'timestamp', 'throttle_1'),
            DataSpec('501', 'timestamp', 'throttle_2', line_color='w')
            ]
        self.placeNewGraph("Throttle", throttleLine, (2, 1))


class CANTableLayout(ReadoutLayout):
    def __init__(self, moduleManager, parent=None):
        super().__init__(moduleManager, parent=parent)

        self.placeCANSender()

        self.table = self.placeCANTable()
        self.table.update_table.connect(self.on_data_ready)

    def on_data_ready(self, data):
        for r, row in enumerate(data):
            for c, cell in enumerate(row):
                self.table.table.setItem(r, c, cell)
