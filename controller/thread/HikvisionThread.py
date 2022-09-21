from curses.ascii import US
from sqlite3 import connect
from time import sleep
from PySide2.QtCore import QThread, Signal
from services.hikvision import isapiClient
from serial import SerialException
from constant.const import HIKVISION_IP, HIKVISION_HOST, HIKVISION_ID, HIKVISION_PASSWORD
import subprocess
import os

class HikvisionThread(QThread):
    hikvision_signal = Signal(bool)
    def __init__(self):
        super().__init__()
        self.__hikivision_service = isapiClient(HIKVISION_HOST, HIKVISION_ID, HIKVISION_PASSWORD)

    def connectHikvision(self):
        self.valid = self.__hikivision_service._check_session()
    
    @staticmethod
    def isConnect():
        res = subprocess.call(["ping", HIKVISION_IP, "-c1", "-W2", "-q"], stdout=open(os.devnull, 'w'))
        if res == 0 : return True
        else: return False

    def run(self):
        while(1):
            if not self.isConnect():
                self.hikvision_signal.emit(False)
            else:    
                self.connectHikvision()
                self.hikvision_signal.emit(True)
            sleep(1)