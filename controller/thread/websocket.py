from curses.ascii import US
from sqlite3 import connect
from time import sleep
from PySide2.QtCore import QThread, Signal

class WebsocketThread(QThread):
    reconnect_signal = Signal()
    def __init__(self):
        super().__init__()
        self.reconnect_status = 0

    def run(self):
        while(1):
            if self.reconnect_status == 1:
                print("Emitting Reconnect Signal")
                self.reconnect_signal.emit()
            sleep(1)