import pyqtgraph as pg
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGridLayout, QHeaderView
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QPainter, QColor
import time


# TODO create general data module class to handle multiple types of data
class DataModule(QObject):
    def __init__(self):
        super().__init__()
        self.title = "N/A"
        self.type = "Empty"
        pass

    def addDataPoint(self, *args):
        raise NotImplementedError('subclasses must override addDataPoint()!')


def timestamp():
    return time.time()


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        try:
            vals = [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S") for value in values]
            return vals
        except Exception:
            return[]


class TimeGraph(DataModule):
    def __init__(self, title, lineSpecs, data_range):

        self.plotItem = pg.PlotWidget(title=title, axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        self.xVals = []
        self.yVals = []
        self.maxPoints = 100
        self.title = title

        self.plotItem.setYRange(*data_range)

        self.lines = {}
        for spec in lineSpecs:
            self.lines[spec] = (self.plotItem.plot([], pen=spec.pen))

        self.type = "Graph"

    def updateGraph(self):
        for spec, line in self.lines.items():
            line.setData(spec.xVals, spec.yVals)

    
    def addDataPoint(self, data):
        needsUpdate = False
        for spec in [sp for sp in self.lines.keys() if sp.isValidData(data)]:
            x = data[spec.xVal_key]
            y = data[spec.yVal_key]
            spec.addXYPoint((x,y))
            needsUpdate = True
        if needsUpdate:
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


class RawText(DataModule):
    def __init__(self, title, spec):
        self.type = "Raw"
        self.title = title
        self.text = QLabel()
        self.text.setText(title)
        self.spec = spec

    def addDataPoint(self, data):
        if self.spec.isValidData(data):
            value = "N/A"
            if not self.spec.rawData:
                value = data[self.spec.xVal_key]
            else:
                value = data['message']
            
            self.text.setText(self.title + str(value))
        
    def getWidget(self):
        return self.text

class CANTable(DataModule):
    update_table = pyqtSignal(object)

    def __init__(self):
        super().__init__()
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
        self.type = "Table"
        self.nextUpdate = time.time() + 1/30

    def addDataPoint(self, raw_data):
        m_id = int(raw_data['id'], 16)

        if m_id not in self.rawDataCount:
            self.rawDataCount[m_id] = 0
        
        self.rawDataCount[m_id] = self.rawDataCount[m_id] + 1

        self.rawDataList[m_id] = raw_data
        sortedDataList = sorted(self.rawDataList)

        self.table.setRowCount(len(sortedDataList))

        all_rows = []

        for row_index, data_key in enumerate(sortedDataList):

            raw_data_point = self.rawDataList[data_key]
            message = raw_data_point['message']
            byte_length = int(raw_data_point['length'])

            row_cells = []

            QTableWidgetItem('0x' + raw_data_point['id'])
            row_cells.insert(0,  QTableWidgetItem('0x' + raw_data_point['id']))

            
            for i in range(0, 8):
                cell_item = QTableWidgetItem(message[i*2: i*2 + 2])
                if i >= byte_length:
                    cell_item = QTableWidgetItem("-")
                row_cells.insert(i+1, cell_item)

            cur_id = int(raw_data_point['id'], 16)
            count = self.rawDataCount[cur_id]
            row_cells.insert(9,  QTableWidgetItem(str(count)))

            all_rows.append(row_cells)
        if time.time() > self.nextUpdate:
            self.nextUpdate = time.time() + 1/30
            self.update_table.emit(all_rows)
       
    def getWidget(self):
        return self.table

class LightToggle(QWidget):
    def __init__(self, text, parent = None):
        QWidget.__init__(self, parent=None)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setEnabled(1)
        self.resize(200, 100)

    def setEnabled(self, enabled):
        if enabled:
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.green)
            self.setPalette(p)
        else:
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.red)
            self.setPalette(p)



class LightArray(DataModule):
    def __init__(self, dataSpecs):
        super().__init__()
        self.type = "Toggle"
        self.grid = QGridLayout()
        self.buttons = {}

        for i ,spec in enumerate(dataSpecs):
            print(spec.id)
            btn = LightToggle(spec.xVal_key)
            btn.setEnabled(1)
            btn.setFixedWidth(100)
            label = QLabel(spec.xVal_key)
            label.setFixedWidth(60)
            label.setFixedHeight(60)
            self.grid.addWidget(label, i, 1)
            self.grid.addWidget(btn, i, 2)
            self.buttons[spec] = btn


    def addDataPoint(self, data):
        for spec, btn in self.buttons.items():
            if (data['id'] == spec.id):
                btn.setEnabled(data[spec.yVal_key] > 3000)

    def getWidget(self):
        return self.grid

class DataModuleManager():
    def __init__(self):
        self.parsedModules = []
        self.rawModules = []

        self.rawTypes = ["Table", "Raw"]
        self.parsedTypes = ["Graph", "Raw", "Toggle"]

    def manageModule(self, newModule):
        if newModule.type in self.rawTypes:
            self.rawModules.append(newModule)

        if newModule.type in self.parsedTypes:
            self.parsedModules.append(newModule)

    # Called whenever new data is to be pushed
    # any graph which is being displayed
    def onRawDataCallback(self, data):
        for g in self.rawModules:
            g.addDataPoint(data)


    # Called whenever new data is to be pushed
    # any graph which is being displayed
    def onParsedDataCallback(self, target_id, data):
        for g in self.parsedModules:
            g.addDataPoint(data)
