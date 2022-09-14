# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)


from PySide2.QtGui import (QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget, QAction)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.navigateSettings = QAction(MainWindow)
        self.navigateSettings.setObjectName(u"navigateSettings")
        self.navigateRegister = QAction(MainWindow)
        self.navigateRegister.setObjectName(u"navigateRegister")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_saldo = QHBoxLayout()
        self.frame_saldo.setObjectName(u"frame_saldo")
        self.saldo = QLabel(self.centralwidget)
        self.saldo.setObjectName(u"saldo")
        font = QFont()
        font.setPointSize(29)
        self.saldo.setFont(font)

        self.frame_saldo.addWidget(self.saldo)

        self.biaya = QLabel(self.centralwidget)
        self.biaya.setObjectName(u"biaya")
        self.biaya.setFont(font)

        self.frame_saldo.addWidget(self.biaya)

        self.frame_saldo.setStretch(0, 1)
        self.frame_saldo.setStretch(1, 3)

        self.verticalLayout.addLayout(self.frame_saldo)

        self.frame_sisa_saldo = QHBoxLayout()
        self.frame_sisa_saldo.setObjectName(u"frame_sisa_saldo")
        self.label_sisa_saldo = QLabel(self.centralwidget)
        self.label_sisa_saldo.setObjectName(u"label_sisa_saldo")
        font1 = QFont()
        font1.setPointSize(33)
        self.label_sisa_saldo.setFont(font1)

        self.frame_sisa_saldo.addWidget(self.label_sisa_saldo)

        self.value_sisa_saldo = QLabel(self.centralwidget)
        self.value_sisa_saldo.setObjectName(u"value_sisa_saldo")
        self.value_sisa_saldo.setFont(font)

        self.frame_sisa_saldo.addWidget(self.value_sisa_saldo)

        self.frame_sisa_saldo.setStretch(0, 1)
        self.frame_sisa_saldo.setStretch(1, 3)

        self.verticalLayout.addLayout(self.frame_sisa_saldo)

        self.frame_main = QHBoxLayout()
        self.frame_main.setObjectName(u"frame_main")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.frame_main.addWidget(self.label)

        self.layout_data = QVBoxLayout()
        self.layout_data.setObjectName(u"layout_data")
        self.label_nama = QLabel(self.centralwidget)
        self.label_nama.setObjectName(u"label_nama")
        font2 = QFont()
        font2.setPointSize(16)
        self.label_nama.setFont(font2)
        self.label_nama.setAlignment(Qt.AlignCenter)

        self.layout_data.addWidget(self.label_nama)

        self.value_nama = QLabel(self.centralwidget)
        self.value_nama.setObjectName(u"value_nama")

        self.layout_data.addWidget(self.value_nama)

        self.label_uid = QLabel(self.centralwidget)
        self.label_uid.setObjectName(u"label_uid")
        self.label_uid.setFont(font2)
        self.label_uid.setAlignment(Qt.AlignCenter)

        self.layout_data.addWidget(self.label_uid)

        self.value_uid = QLabel(self.centralwidget)
        self.value_uid.setObjectName(u"value_uid")

        self.layout_data.addWidget(self.value_uid)


        self.frame_main.addLayout(self.layout_data)


        self.verticalLayout.addLayout(self.frame_main)

        self.frame_status = QHBoxLayout()
        self.frame_status.setObjectName(u"frame_status")
        self.status_internet = QLabel(self.centralwidget)
        self.status_internet.setObjectName(u"status_internet")

        self.frame_status.addWidget(self.status_internet)

        self.status_gate = QLabel(self.centralwidget)
        self.status_gate.setObjectName(u"status_gate")

        self.frame_status.addWidget(self.status_gate)

        self.status_cctv = QLabel(self.centralwidget)
        self.status_cctv.setObjectName(u"status_cctv")

        self.frame_status.addWidget(self.status_cctv)

        self.status_rfid = QLabel(self.centralwidget)
        self.status_rfid.setObjectName(u"status_rfid")

        self.frame_status.addWidget(self.status_rfid)


        self.verticalLayout.addLayout(self.frame_status)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 10)
        self.verticalLayout.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.navigateSettings)
        self.menuMenu.addAction(self.navigateRegister)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.navigateSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.navigateRegister.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.saldo.setText(QCoreApplication.translate("MainWindow", u"Saldo Awal : ", None))
        self.biaya.setText(QCoreApplication.translate("MainWindow", u"Biaya", None))
        self.label_sisa_saldo.setText(QCoreApplication.translate("MainWindow", u"Sisa Saldo :", None))
        self.value_sisa_saldo.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText("")
        self.label_nama.setText(QCoreApplication.translate("MainWindow", u"Nama", None))
        self.value_nama.setText("")
        self.label_uid.setText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.value_uid.setText("")
        self.status_internet.setText(QCoreApplication.translate("MainWindow", u"Gate : Connected", None))
        self.status_gate.setText(QCoreApplication.translate("MainWindow", u"Status : Online", None))
        self.status_cctv.setText(QCoreApplication.translate("MainWindow", u"CCTV : Connected", None))
        self.status_rfid.setText(QCoreApplication.translate("MainWindow", u"RFID : Connected", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi

