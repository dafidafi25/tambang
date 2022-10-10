import json
from os import stat
from controller.thread.ApiServices import ApiServices
from view.Dashboard import Ui_Dashboard
from PySide2.QtWidgets import QMainWindow

from PySide2.QtGui import QPixmap, QColor,QPixmap
from PySide2 import QtGui
from PySide2 import QtCore

from .thread.GateThread import GateThread
from .thread.HikvisionThread import HikvisionThread
from .thread.SmartCardThread import SmartCardThread
from .thread.websocket  import WebsocketThread

from .AddMenu import DialogAddSaldo
from .RegisterMenu import DialogRegister
from .Setting import DialogSetting

from PySide2 import QtCore, QtWebSockets, QtNetwork, QtGui
from PySide2.QtCore import QUrl

import cv2
import numpy as np

from constant.const import HIKVISION_HOST,HIKVISION_ID,HIKVISION_IP,GATE_ADDRESS,GATE_BAUD_RATE,GATE_USB_PORT


class DashboardController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui  = Ui_Dashboard()

        self.ui.setupUi(self)

        grey = QPixmap(500,401)
        grey.fill(QColor('darkgray'))

        self.ui.value_camera.setPixmap(grey)

        ## Register Thread
        self.gate_thread = GateThread(GATE_ADDRESS, GATE_BAUD_RATE)
        self.gate_thread.start()
        self.rfid_thread = SmartCardThread()
        self.rfid_thread.start()
        self.hikvision_thread = HikvisionThread()
        self.hikvision_thread.start()
        self.websocket_thread = WebsocketThread()
        self.websocket_thread.start()

        self.gate_thread.connect_signal.connect(self.__gate_status)
        
        self.hikvision_thread.hikvision_signal.connect(self.__hikvision_status)   
        self.websocket_thread.reconnect_signal.connect(self.webSocketSignal)

        self.api_services = ApiServices()

        response = self.api_services.getImageCam()
    
        image = np.asarray(bytearray(response), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cvt_img = self.convert_cv_qt(image,640,480)
        self.ui.value_camera.setPixmap(cvt_img)

        #web socket#
        self.client =  QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)
        self.client.error.connect(self.onError)
        self.client.open(QUrl("ws://10.13.2.106:6000/gate"))
        self.client.connected.connect(self.onConnect)
        self.client.textMessageReceived.connect(self.onMessageReceived)
        self.client.disconnected.connect(self.onDisconnect)

        #prepare Dialog
        self.dialog_add_saldo = None
        self.dialog_register = None
        self.dialog_settings = None

        self.__initialize_button()
    
    def __initialize_button(self):
        self.ui.navigateAddSaldo.triggered.connect(self.__open_dialog_add_saldo)
        self.ui.navigateRegister.triggered.connect(self.__open_dialog_register)
        self.ui.navigateSettings.triggered.connect(self.__open_dialog_settings)
    
    def webSocketSignal(self):
        print("Web Socket Reconnecting ....")
        self.client.open(QUrl("ws://10.13.2.106:6000/gate"))
    
    def onConnect(self):
        print("Web Socket Connected")
        try:
            self.websocket_thread.reconnect_status = 0
        except Exception as err:
            print(err)

    def onDisconnect(self):
        print("Web Socket Disconnected")
        self.websocket_thread.reconnect_status = 1


    def onError(self, msg):
        print(msg)
    
    def onPong(self, elapsedTime, payload):
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))
    
    def onMessageReceived(self,data):
        if self.gate_thread.__is_connected :
            data = json.loads(data)
            self.ui.status_internet.setText(data['price'])
            actual_gate = self.gate_thread.getGateStatus()
            if data['gate'] == 1 and actual_gate != 1 : 
                self.gate_thread.openGate()

            elif data['gate'] == 0 and actual_gate != 0 : 
                self.gate_thread.closeGate()

        pass

    def __open_dialog_add_saldo(self):
        self.rfid_thread.read_mode = 0
        self.dialog_add_saldo = DialogAddSaldo(self.rfid_thread)
        self.dialog_add_saldo.start()
        self.rfid_thread.read_mode = 1
        pass

    def __open_dialog_register(self):
        self.rfid_thread.read_mode = 0
        self.dialog_register = DialogRegister(self.rfid_thread)
        self.dialog_register.start()
        self.rfid_thread.read_mode = 1
        pass

    def __open_dialog_settings(self):
        self.rfid_thread.read_mode = 0
        self.dialog_settings = DialogSetting(self.gate_thread)
        self.dialog_settings.start()
        self.rfid_thread.read_mode = 1
        pass
    
    def __card_signal(self,tag):
        data = self.api_services.getByUid(tag)
        price = self.ui.status_internet.text()
        print(data)
        if "saldo" not in data : return
        

        if int(data['saldo']) >= int(price) and self.gate_thread.gate_status == 0:
            self.api_services.openGate()
            sisa = str(int(data['saldo']) - int(price))
            self.ui.value_sisa_saldo.setText(sisa) 
            self.ui.value_nama.setText(data['username'])
            self.ui.value_email.setText(data['email'])
            self.ui.value_phone.setText(data['phone'])
            self.ui.value_saldo.setText(data['saldo'])
            self.ui.value_biaya.setText(price)

            response = self.api_services.getImageCam()
            image = np.asarray(bytearray(response), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cvt_img = self.convert_cv_qt(image,640,480)
            self.ui.value_camera.setPixmap(cvt_img)
            self.api_services.setSaldo(sisa,data['UID'])
            self.api_services.addTransaction(data['id'], price)


        # print(img)
        # ba = QtCore.QByteArray.fromBase64(img)
        # print(ba)
        # pixmap = QPixmap()
        # pixmap.loadFromData(ba)
        # self.ui.value_camera.setPixmap(pixmap)

        pass

    def convert_cv_qt(self, img, widht, height):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(widht, height, QtCore.Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def __hikvision_status(self,isConnected):
        if isConnected: self.ui.status_cctv.setText("CCTV : Connected")
        else : self.ui.status_cctv.setText("CCTV Disconnected")
        pass

    def __gate_status(self,isConnected):
        self.client.sendTextMessage('{"gate": "Sending Gate Status Request"}')
        if isConnected: self.ui.status_gate.setText("GATE : Connected")
        else : self.ui.status_gate.setText("GATE : Disconnected")
        pass

    def __smart_card_status(self,isConnected):
        if isConnected: self.ui.status_rfid.setText("RFID : Connected")
        else : self.ui.status_rfid.setText("RFID : Disconnected")
        pass

    def __price_status(self,price):
        print(price)
        pass

    def start(self):
        self.show()