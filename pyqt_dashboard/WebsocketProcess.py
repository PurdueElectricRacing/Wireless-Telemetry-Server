import time
from PyQt5.QtCore import QThread
import CANWebsocketClient


class WebsocketProcess(QThread):

    def __init__(self, dataManager):
        QThread.__init__(self)
        self.dataManager = dataManager
        self.isDebug = False
        self.client = CANWebsocketClient.CANWebsocketClient(
            self.appendToBuffer,
            self.on_close,
            self.isDebug)
        self.buffer = []

    def __del__(self):
        self.wait()

    def appendToBuffer(self, data):
        for message in data:
            time = float(message['ts'])
            self.dataManager.onRawDataCallback(message)
            parsed = CANWebsocketClient.parseRawMessage(message, time)

            if parsed['parsed']:
                m_id = parsed['id']
                self.dataManager.onParsedDataCallback(m_id, parsed)

    def run(self):
        if self.isDebug:
            self.client.start("ws://127.0.0.1:5000")
        else:
            self.client.start("ws://192.168.4.1:5000")

    def on_close(self):
        self.connected = False
        pass
