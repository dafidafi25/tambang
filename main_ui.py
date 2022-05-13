# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from time import sleep
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal, QThread)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

from smartCard2 import smartCard
from gateMX50 import gate
SECTOR = [4*0,4*1,4*2,4*3,4*4,4*5,4*6,4*7,4*8,4*9,4*10,4*11,4*12,4*13,4*14,4*15]
from Enum import GateSetting
from Authentication import AESCipher
from smartcard.util import toHexString
import requests
from smtpMail import sendEmail

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

settings = []
url_offline = "http://192.168.1.100:6000/api"
url_online = ""
with open('setting.txt') as f:
    settings = f.readlines()

for setting in settings:
    menuName = setting[0:setting.index("=")]
    
    if menuName == GateSetting.BAUD_RATE.value:

        BAUD_RATE =setting[setting.index("=")+1: len(setting)-1]

    if menuName == GateSetting.USB_PORT.value:
        USB_PORT = setting[setting.index("=")+1: len(setting)-1]
        
    if menuName == GateSetting.GATE_ADDRESS.value:
        GATE_ADDRESS = setting[setting.index("=")+1: len(setting)]

gateControl = gate(GATE_ADDRESS=int(GATE_ADDRESS),BAUD_RATE= BAUD_RATE,USB_PORT=USB_PORT)


class WorkerThread(QThread):
    reader_signal = Signal(object)

    def run(self):
        self.smartcard = smartCard()
        self.smartcard.connect()
        self.endpoint = []
        try :
            self.smartReader = smartCard()
            deviceConnected = self.smartReader.connect()
            assert deviceConnected, "Device Not Connected"

        except AssertionError as msg:
            print(msg)

        except Exception as e:
            print(e)
            listSmartReader= []
        while True:
            if deviceConnected:
                gateControlStatus = gateControl.getGateStatus()
                cardValue = []
                if(len(gateControlStatus) > 0 ):
                    status = [x for x in gateControlStatus]
                    status = True if status[1] == 12  else False
                else:
                    status = False
                
                if(self.smartReader.isNewCard()):
                    if(status):
                        cardValue = self.smartReader.readCard()
                    else:
                        print("Gate")
                if cardValue:
                    valid = requests.post(url_offline+"/validate/uid",json={
                        "uid": AESCipher(key2).encrypt(cardValue)
                    }).json()
                    if valid:
                        # result = db.getUserByUid(AESCipher(key2).encrypt(cardValue))
                        result = requests.post(url_offline+"/get/user/uid",json={
                            "uid": AESCipher(key2).encrypt(cardValue)
                        }).json()
                        saldo = result[0]['saldo']
                        id = result[0]['id']
                        uid = result[0]['UID']
                        # price = db.getDevicePrice()[0]['price']
                        gate_data = requests.get(url_offline+"/price/get").json()
                        price = gate_data[0]["price"]
                        username = result[0]['username']
                        phone = result[0]['phone']
                        email = result[0]['email']


                        if saldo > int(price):
                            newSaldo = saldo -int(price)
                            keyA = result[0]['keyA']
                            key_access = AESCipher(str(saldo)).decrypt(keyA).decode('utf-8')
                            wallet_format,key_access = self.smartReader.getValueBlockFormat(newSaldo,SECTOR[10]+1)
                            gateControl.openGate()
                            requests.post(url_offline+"/transaction",json={
                                "id": id,
                                "plate_number": "",
                                "price" : price
                            }).json()

                            requests.post(url_offline+"/saldo",json={
                                "key": AESCipher(str(newSaldo)).encrypt(toHexString(key_access)),
                                "uid" : uid,
                                "saldo" : newSaldo


                            }).json()
                            print(newSaldo)
                            # db.updateSaldo(AESCipher(str(newSaldo)).encrypt(toHexString(key_access)),uid,newSaldo)
                            self.smartReader.setWalletSector(newSaldo,SECTOR[10])
                            self.checkSaldo()
                            self.reader_signal.emit({
                                "price":price,
                                "newSaldo":newSaldo,
                                "status" : 1,
                                "username" : username,
                                "phone" : phone,
                                "email": email

                            })
                    cardValue = False
            sleep(1)
    
    def checkSaldo(self):
        authB = [0xff,0xff,0xff,0xff,0xff,0xff]
        self.smartReader.setTempAuth(1,authB)
        print(self.smartReader.readBlock(SECTOR[10],16,1))
    
    # def check
        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        mainFont = QFont("Times New Roman",40)
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(30, 20, 721, 311))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.layout_atas = QHBoxLayout()
        self.layout_atas.setObjectName(u"layout_atas")
        self.UID_value = QLabel(self.verticalLayoutWidget)
        self.UID_value.setObjectName(u"UID_value")
        self.UID_value.setAlignment(Qt.AlignCenter)

        self.layout_atas.addWidget(self.UID_value)

        self.UID_text = QLabel(self.verticalLayoutWidget)
        self.UID_text.setObjectName(u"UID_text")
        self.UID_text.setBaseSize(QSize(0, 0))
        self.UID_text.setScaledContents(False)
        self.UID_text.setAlignment(Qt.AlignCenter)

        self.layout_atas.addWidget(self.UID_text)


        self.verticalLayout.addLayout(self.layout_atas)

        self.layout_bawah = QHBoxLayout()
        self.layout_bawah.setObjectName(u"layout_bawah")
        self.SIS_value = QLabel(self.verticalLayoutWidget)
        self.SIS_value.setObjectName(u"SIS_value")
        self.SIS_value.setAlignment(Qt.AlignCenter)

        self.layout_bawah.addWidget(self.SIS_value)

        self.SISA_text = QLabel(self.verticalLayoutWidget)
        self.SISA_text.setObjectName(u"SISA_text")
        self.SISA_text.setAlignment(Qt.AlignCenter)

        self.layout_bawah.addWidget(self.SISA_text)


        self.verticalLayout.addLayout(self.layout_bawah)

        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(30, 370, 721, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Status_Label = QLabel(self.horizontalLayoutWidget_3)
        self.Status_Label.setObjectName(u"Status_Label")
        self.Status_Label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.Status_Label)

        self.label = QLabel(self.horizontalLayoutWidget_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.pushButton = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.resize(300,300)
        self.pushButton.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)
        self.horizontalLayoutWidget_4 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(30, 490, 721, 81))

        self.detaillayout = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.detaillayout.setObjectName(u"detaillayout")
        self.detaillayout.setContentsMargins(0, 0, 0, 0)
        self.layout_username = QVBoxLayout()
        self.layout_username.setObjectName(u"layout_username")
        self.label_nama = QLabel(self.horizontalLayoutWidget_4)
        self.label_nama.setObjectName(u"label_nama")
        self.label_nama.setAlignment(Qt.AlignCenter)

        self.layout_username.addWidget(self.label_nama)

        self.value_nama = QLabel(self.horizontalLayoutWidget_4)
        self.value_nama.setObjectName(u"value_nama")
        self.value_nama.setAlignment(Qt.AlignCenter)

        self.layout_username.addWidget(self.value_nama)

        self.detaillayout.addLayout(self.layout_username)

        self.layout_phone = QVBoxLayout()
        self.layout_phone.setObjectName(u"layout_phone")
        self.label_phone = QLabel(self.horizontalLayoutWidget_4)
        self.label_phone.setObjectName(u"label_phone")
        self.label_phone.setAlignment(Qt.AlignCenter)

        self.layout_phone.addWidget(self.label_phone)

        self.value_phone = QLabel(self.horizontalLayoutWidget_4)
        self.value_phone.setObjectName(u"value_phone")
        self.value_phone.setAlignment(Qt.AlignCenter)

        self.layout_phone.addWidget(self.value_phone)


        self.detaillayout.addLayout(self.layout_phone)

        self.layout_email = QVBoxLayout()
        self.layout_email.setObjectName(u"layout_email")
        self.label_email = QLabel(self.horizontalLayoutWidget_4)
        self.label_email.setObjectName(u"label_email")
        self.label_email.setAlignment(Qt.AlignCenter)

        self.layout_email.addWidget(self.label_email)

        self.value_email = QLabel(self.horizontalLayoutWidget_4)
        self.value_email.setObjectName(u"value_email")
        self.value_email.setAlignment(Qt.AlignCenter)

        self.layout_email.addWidget(self.value_email)


        self.detaillayout.addLayout(self.layout_email)



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.UID_text.setFont(QFont("Times New Roman",40))
        self.UID_value.setFont(QFont("Times New Roman",40))
        self.UID_text.setStyleSheet("background-color:#D3D3D3")
        self.SISA_text.setStyleSheet("background-color:#D3D3D3")
        self.SIS_value.setFont(QFont("Times New Roman",40))
        self.SISA_text.setFont(QFont("Times New Roman",40))
        self.Status_Label.setFont(QFont("Times New Roman",20))
        self.label.setFont(QFont("Times New Roman",20))
        self.pushButton.setFont(QFont("Times New Roman",20))
        self.pushButton_2.setFont(QFont("Times New Roman",20))

        self.pushButton.clicked.connect(self.ack)
        self.pushButton_2.clicked.connect(self.emergency)
        
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.worker = WorkerThread()
        self.worker.start()
        self.worker.reader_signal.connect(self.detectedCard)
        


    # setupUi

    def retranslateUi(self, MainWindow):
        
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.UID_value.setText(QCoreApplication.translate("MainWindow", u"Biaya", None))
        self.UID_text.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.SIS_value.setText(QCoreApplication.translate("MainWindow", u"Sisa Saldo", None))
        self.SISA_text.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.Status_Label.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Berhasil / gagal", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"ACK", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Trouble", None))
        self.label_nama.setText(QCoreApplication.translate("MainWindow", u"nama", None))
        self.value_nama.setText(QCoreApplication.translate("MainWindow", u"value nama", None))
        self.label_phone.setText(QCoreApplication.translate("MainWindow", u"phone", None))
        self.value_phone.setText(QCoreApplication.translate("MainWindow", u"value phone", None))
        self.label_email.setText(QCoreApplication.translate("MainWindow", u"email", None))
        self.value_email.setText(QCoreApplication.translate("MainWindow", u"value email", None))
    
    def detectedCard(self,data):
        price = data['price']
        newSaldo = data['newSaldo']
        status = data['status']
        username = data['username']
        phone = data['phone']
        email = data['email']
        
        self.UID_text.setText(price)
        self.SISA_text.setText(str(newSaldo))
        self.label.setText("Berhasil" if status == 1 else "Gagal")
        self.value_nama.setText(username)
        self.value_phone.setText(phone)
        self.value_email.setText(email)
    
    def ack(self):

        self.UID_text.setText("")
        self.SISA_text.setText("")
        self.label.setText("")
        self.value_nama.setText("")
        self.value_phone.setText("")
        self.value_email.setText("")
        

    def emergency(self):
        self.UID_text.setText("")
        self.SISA_text.setText("")
        self.label.setText("")
        self.value_nama.setText("")
        self.value_phone.setText("")
        self.value_email.setText("")
        sendEmail()
        


    # retranslateUi

