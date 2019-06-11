import time
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QInputDialog

from CANWebsocketClient import *


class WebsocketProcess(QThread):
    def __init__(self, dataManager, ip, isDebug=False):
        QThread.__init__(self)
        self.dataManager = dataManager
        self.isDebug = isDebug
        self.ip = ip
        self.client = CANWebsocketClient(
            self.appendToBuffer,
            self.on_close,
            self.isDebug)
        self.buffer = []

    def __del__(self):
        self.wait()

    def appendToBuffer(self, data):

        # if not isinstance(data, list):
        #     data = [data]
        for m_id in data:
            message = data[m_id]
            time = float(message['ts'])
 
            self.dataManager.onRawDataCallback(message)

            parsed = self.client.parseRawMessage(message, time)

            if parsed['parsed']:
                m_id = parsed['id']
                self.dataManager.onParsedDataCallback(m_id, parsed)

    def run(self):
        self.client.start(self.ip)

    def on_close(self):
        self.connected = False
        print("Closed!")
        pass
