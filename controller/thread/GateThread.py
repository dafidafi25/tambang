from curses.ascii import US
from sqlite3 import connect
from time import sleep
from PySide2.QtCore import QThread, Signal
from controller.thread.ApiServices import ApiServices
from services.gateMX50 import gate
from serial import SerialException

from PySide2 import QtCore, QtWebSockets, QtNetwork, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PySide2.QtCore import QUrl

import asyncio
import websockets

class GateThread(QThread):
    connect_signal = Signal(bool)
    def __init__(self,GATE_ADDRESS,BAUD_RATE):
        super().__init__()
        self.GATE_ADDRESS = GATE_ADDRESS
        self.BAUD_RATE = BAUD_RATE
        self.USB_PORT = None
        self.__gate_services =  gate(self.GATE_ADDRESS,self.BAUD_RATE)
        self.apiServices = ApiServices()     
        self.__is_connected = False
        self.gate_status = 0


    
    def openGate(self):
        self.__gate_services.openGate()
    
    def closeGate(self):
        self.__gate_services.closeGate()
    
    def reset(self):
        self.__is_connected = False
    
    def run(self):
        
        while(True):
            if self.__gate_services.serial_ports():
                
                if not self.__is_connected:
                    try:
                        self.__gate_services.connectGate()
                        self.__is_connected = True
                        
                    except Exception as err:
                        print(err)
                else:
                    self.connect_signal.emit(True)

            else:
                self.reset()
                
                self.connect_signal.emit(False)

            sleep(0.5)
