from curses.ascii import US
from sqlite3 import connect
from time import sleep
from PySide2.QtCore import QThread, Signal
from services.gateMX50 import gate
from serial import SerialException

class GateThread(QThread):
    connect_signal = Signal(bool)
    def __init__(self,GATE_ADDRESS,BAUD_RATE,USB_PORT):
        super().__init__()
        self.GATE_ADDRESS = GATE_ADDRESS
        self.BAUD_RATE = BAUD_RATE
        self.USB_PORT = USB_PORT
        self.__gate_services =  gate(self.GATE_ADDRESS,self.BAUD_RATE, self.USB_PORT)
        
        self.__is_connected = False
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
