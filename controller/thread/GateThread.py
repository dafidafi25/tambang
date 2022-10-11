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
        self.is_connected = False

        self.__is_sync = False
    
    def openGate(self):
        self.__gate_services.openGate()
        self.apiServices.openGate()
    
    def getGateStatus(self):
        response = self.__gate_services.getGateStatus()

        if len(response) < 1 : return False
        status = response[1]

        if status == 9 : return True
        elif status == 12 : return False
        print("Status is not Valid")
        return None
            
    
    def closeGate(self):
        self.__gate_services.closeGate()
        self.apiServices.closeGate()
    
    def reset(self):
        self.is_connected = False
    
    def run(self):
        while(True):
            if self.__gate_services.serial_ports():
                if not self.is_connected:
                    try:
                        self.__gate_services.connectGate()
                        self.is_connected = True 

                        if not self.__is_sync:
                            gate_status = self.getGateStatus()
                            if gate_status : self.apiServices.openGate()
                            else: self.apiServices.closeGate()
                            
                            self.__is_sync = True
                            
                    except Exception as err:
                        print(err)
                else:
                    if not self.__is_sync:
                            gate_status = self.getGateStatus()
                            if gate_status : self.apiServices.openGate()
                            else: self.apiServices.closeGate()
                            
                            self.__is_sync = True
                    self.connect_signal.emit(True)
            else:
                self.reset()
                self.connect_signal.emit(False)
            sleep(0.5)
