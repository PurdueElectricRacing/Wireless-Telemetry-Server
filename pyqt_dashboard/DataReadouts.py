import pyqtgraph as pg
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QLabel, \
                            QVBoxLayout, QHBoxLayout, QWidget, QPushButton,\
                            QGridLayout, QHeaderView
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor, \
                        QPalette, QGraphicsView
import time
from CAN_Logger import *


class DataSpec():
    def __init__(self, m_id, xVal_key, yVal_key,
                 line_color='r', rawData=False):
        self.id = m_id
        self.xVal_key = xVal_key
        self.yVal_key = yVal_key

        self.xVals = []
        self.yVals = []

        self.maxPoints = 150

        self.pen = pg.mkPen(width=4.5, color=line_color)
        self.rawData = rawData

    def addXYPoint(self, point):
        x, y = point
        self.xVals.append(x)
        self.yVals.append(y)

        self.xVals = self.xVals[-self.maxPoints:]
        self.yVals = self.yVals[-self.maxPoints:]

    def isValidData(self, data):
        return (data['i'] == self.id and self.rawData) or \
               (data['i'] == self.id and
                self.xVal_key in data and
                self.yVal_key in data)

    def isSemiValidData(self, data):
        return (data['i'] == self.id and self.rawData)


class DataModule(QObject):
    def __init__(self, dataSpecs):
        super().__init__()
        self.title = "N/A"
        self.dataSpecs = dataSpecs

    def addDataPoint(self, *args):
        raise NotImplementedError('subclasses must override addDataPoint()!')

    def getDataSpecs(self):
        return self.dataSpecs


def timestamp():
    return time.time()


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        try:
            vals = [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S")
                    for value in values]
            return vals
        except Exception:
            return[]


class TimeGraph(DataModule):
    def __init__(self, title, lineSpecs, data_range):
        super().__init__(lineSpecs)
        self.plotItem = pg.PlotWidget(title=title, axisItems={'bottom':
                                      TimeAxisItem(orientation='bottom')})

        self.maxPoints = 100
        self.updateRate = 1/20
        self.lastUpdate = time.time()
        self.title = title

        self.plotItem.setYRange(*data_range)

        self.lines = {}
        self.plotItem.addLegend()
        for spec in lineSpecs:
            self.lines[spec] = self.plotItem.plot([],
                                                  pen=spec.pen,
                                                  name=spec.yVal_key,
                                                  autoDownsample=True)

        self.plotItem.setMouseEnabled(x=False, y=False)
        self.plotItem.showGrid(x=False, y=True, alpha=0.5)

        self.isPaused = False
        self.plotItem.scene().sigMouseClicked.connect(self.togglePaused)

    def togglePaused(self):
        self.isPaused = not self.isPaused

    def updateGraph(self):
        if not self.isPaused:
            for spec, line in self.lines.items():
                line.setData(spec.xVals, spec.yVals)

    def addDataPoint(self, data):
        needsUpdate = False

        for spec in self.lines.keys():
            x = data[spec.xVal_key]
            y = data[spec.yVal_key]
            spec.addXYPoint((x, y))
            needsUpdate = True

        if needsUpdate and self.lastUpdate + self.updateRate < time.time():
            self.lastUpdate = time.time()
            self.updateGraph()

    def getWidget(self):
        return self.plotItem


class RawText(DataModule):
    def __init__(self, title, spec):
        super().__init__([spec])
        self.title = title
        self.text = QLabel()
        self.text.setText(title)
        self.spec = spec

    def addDataPoint(self, data):
        value = "N/A"
        if self.spec.rawData:
            value = data['data']
        else:
            value = data[self.spec.xVal_key]

        self.text.setText(self.title + str(value))

    def getWidget(self):
        return self.text


class CANTable(DataModule):
    update_table = pyqtSignal(object)

    def __init__(self):
        super().__init__([])
        self.table = QTableWidget(0, 0)
        self.table.verticalHeader().setVisible(False)

        col_headers = ['ID']
        for i in range(0, 8):
            col_headers.append('Byte ' + str(i))
        col_headers.append('Count')

        self.table.setColumnCount(len(col_headers))
        self.table.setHorizontalHeaderLabels(col_headers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1)

        self.rawDataList = {}
        self.rawDataCount = {}
        self.updateRate = 1/20
        self.nextUpdate = time.time() + self.updateRate

    def addDataPoint(self, raw_data):
        m_id = int(raw_data['i'], 16)

        log_CAN_data(m_id, raw_data['m'])

        if m_id not in self.rawDataCount:
            self.rawDataCount[m_id] = 0

        self.rawDataCount[m_id] = self.rawDataCount[m_id] + 1

        self.rawDataList[m_id] = raw_data
        sortedDataList = sorted(self.rawDataList)

        self.table.setRowCount(len(sortedDataList))

        all_rows = []

        for row_index, data_key in enumerate(sortedDataList):

            raw_data_point = self.rawDataList[data_key]
            message = raw_data_point['m']
            byte_length = len(message)

            row_cells = []

            QTableWidgetItem('0x' + raw_data_point['i'])
            row_cells.insert(0,  QTableWidgetItem('0x' + raw_data_point['i']))

            for i in range(0, 8):
                cell_item = QTableWidgetItem(message[i*2: i*2 + 2])
                if i >= byte_length:
                    cell_item = QTableWidgetItem("-")
                row_cells.insert(i+1, cell_item)

            cur_id = int(raw_data_point['i'], 16)
            count = self.rawDataCount[cur_id]
            row_cells.insert(9,  QTableWidgetItem(str(count)))

            all_rows.append(row_cells)
        if time.time() > self.nextUpdate:
            self.nextUpdate = time.time() + self.updateRate
            self.update_table.emit(all_rows)

    def getWidget(self):
        return self.table


class LightToggle(QPushButton):
    def __init__(self, text, parent=None):
        QWidget.__init__(self, parent=None)
        self.isEnabled = -1

        self.maxRate = 100/1000
        self.lastTime = time.time()
        self.setEnabled(1)

    def setEnabled(self, enabled):
        if enabled == self.isEnabled:
            return

        if self.lastTime + self.maxRate > time.time():
            self.lastTime = time.time()
        
            self.isEnabled = enabled

            if self.isEnabled:
                self.setStyleSheet("background-color: green")
            else:
                self.setStyleSheet("background-color: red")


class LightArray(DataModule):
    def __init__(self, dataSpecs):
        super().__init__(dataSpecs)
        self.vBox = QVBoxLayout()
        self.grid = QGridLayout()
        self.buttons = {}

        for i, spec in enumerate(dataSpecs):
            btn = LightToggle(spec.xVal_key)
            label = QLabel(spec.xVal_key)

            btn.setFixedWidth(50)
            btn.setFixedHeight(50)
            label.setFixedWidth(60)
            label.setFixedHeight(50)
            
            self.grid.addWidget(label, i, 1)
            self.grid.addWidget(btn, i, 2)
            self.buttons[spec] = btn

        self.vBox.addLayout(self.grid)
        self.vBox.addStretch()

    def addDataPoint(self, data):
        for spec, btn in self.buttons.items():
            if (data['id'] == spec.id):
                btn.setEnabled(data[spec.yVal_key] > 0)

    def getWidget(self):
        return self.vBox


class DataModuleManager():
    def __init__(self):

        self.rawModules = []
        self.subscribedIDs = {}

        self.rawTypes = (CANTable, RawText)
        self.parsedTypes = (TimeGraph, RawText, LightArray)

    def manageModule(self, newModule):

        if isinstance(newModule, self.rawTypes):
            self.rawModules.append(newModule)

        for spec in newModule.getDataSpecs():
            if spec.id not in self.subscribedIDs:
                self.subscribedIDs[spec.id] = [newModule]
            else:
                self.subscribedIDs[spec.id].append(newModule)

    # Called whenever new data is to be pushed
    # any graph which is being displayed
    def onRawDataCallback(self, data):
        for module in self.rawModules:
            module.addDataPoint(data)

    # Called whenever new data is to be pushed
    # any graph which is being displayed
    def onParsedDataCallback(self, target_id, data):
        if target_id in self.subscribedIDs:
            for module in self.subscribedIDs[target_id]:
                module.addDataPoint(data)
