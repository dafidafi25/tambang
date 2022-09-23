from curses.ascii import US
from sqlite3 import connect
from time import sleep
from PySide2.QtCore import QThread, Signal
from constant.const import BASE_URL
from services.gateMX50 import gate
from serial import SerialException
import base64

import requests
from requests.auth import HTTPDigestAuth

class ApiServices(QThread):
    connect_signal = Signal(bool)
    def __init__(self):
        super().__init__()
        self.base_url = BASE_URL
        
    def getByUid(self, tag):
        myobj = {'uid': tag}

        x = requests.post(f'{self.base_url}/get/user/uid', json = myobj)  

        if x.status_code <= 199 and x.status_code >= 300: return {} 
        x = x.json()

        return x
    
    def getImageCam(self):
        imgBase64 = requests.get(f'http://admin:-arngnennscfrer2@192.168.2.64/Streaming/channels/1/picture', auth=HTTPDigestAuth("admin", "-arngnennscfrer2"))
        
        if imgBase64.status_code >= 200 and imgBase64.status_code <= 299:

            return imgBase64.content
    
    def getGateStatus(self):
        response = requests.get(f'{self.base_url}/gate').json()
        return response
    
    def setGateStatus(self, status):
        myObj = {
            'gate_status': status,
            "id": 1
        }
        response = requests.post(f'{self.base_url}/gate/set/gate_status', json=myObj).json()
        return response
    
    def openGate(self):
        myobj = {'gate': 1, 'id':1}
        requests.post(f'{self.base_url}/gate/set/gate', json=myobj)
    
    def closeGate(self):
        myobj = {'gate': 0, 'id':1}
        requests.post(f'{self.base_url}/gate/set/gate', json=myobj)


    
    # def run(self):
    #     while(True):
    #         if self.__gate_services.serial_ports():
                
    #             if not self.__is_connected:
    #                 try:
    #                     self.__gate_services.connectGate()
    #                     self.__is_connected = True
                        
    #                 except Exception as err:
    #                     print(err)
    #             else:
    #                 self.connect_signal.emit(True)

    #         else:
    #             self.reset()
                
    #             self.connect_signal.emit(False)

    #         sleep(0.5)
