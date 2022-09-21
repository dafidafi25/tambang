# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Dashboard.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        if not Dashboard.objectName():
            Dashboard.setObjectName(u"Dashboard")
        Dashboard.resize(1280, 720)
        self.navigateSettings = QAction(Dashboard)
        self.navigateSettings.setObjectName(u"navigateSettings")
        self.navigateRegister = QAction(Dashboard)
        self.navigateRegister.setObjectName(u"navigateRegister")
        self.navigateAddSaldo = QAction(Dashboard)
        self.navigateAddSaldo.setObjectName(u"navigateAddSaldo")
        self.centralwidget = QWidget(Dashboard)
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

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.frame_saldo.addWidget(self.label)

        self.value_biaya = QLabel(self.centralwidget)
        self.value_biaya.setObjectName(u"value_biaya")
        self.value_biaya.setFont(font)

        self.frame_saldo.addWidget(self.value_biaya)

        self.frame_saldo.setStretch(0, 2)
        self.frame_saldo.setStretch(1, 1)
        self.frame_saldo.setStretch(2, 10)

        self.verticalLayout.addLayout(self.frame_saldo)

        self.frame_sisa_saldo = QHBoxLayout()
        self.frame_sisa_saldo.setObjectName(u"frame_sisa_saldo")
        self.label_sisa_saldo = QLabel(self.centralwidget)
        self.label_sisa_saldo.setObjectName(u"label_sisa_saldo")
        font1 = QFont()
        font1.setPointSize(33)
        self.label_sisa_saldo.setFont(font1)

        self.frame_sisa_saldo.addWidget(self.label_sisa_saldo)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.frame_sisa_saldo.addWidget(self.label_2)

        self.value_sisa_saldo = QLabel(self.centralwidget)
        self.value_sisa_saldo.setObjectName(u"value_sisa_saldo")
        self.value_sisa_saldo.setFont(font)

        self.frame_sisa_saldo.addWidget(self.value_sisa_saldo)

        self.frame_sisa_saldo.setStretch(0, 2)
        self.frame_sisa_saldo.setStretch(1, 1)
        self.frame_sisa_saldo.setStretch(2, 10)

        self.verticalLayout.addLayout(self.frame_sisa_saldo)

        self.frame_main = QHBoxLayout()
        self.frame_main.setObjectName(u"frame_main")
        self.value_camera = QLabel(self.centralwidget)
        self.value_camera.setObjectName(u"value_camera")

        self.frame_main.addWidget(self.value_camera)

        self.layout_data = QVBoxLayout()
        self.layout_data.setObjectName(u"layout_data")
        self.layout_nama = QHBoxLayout()
        self.layout_nama.setObjectName(u"layout_nama")
        self.label_nama = QLabel(self.centralwidget)
        self.label_nama.setObjectName(u"label_nama")

        self.layout_nama.addWidget(self.label_nama)

        self.separator_4 = QLabel(self.centralwidget)
        self.separator_4.setObjectName(u"separator_4")

        self.layout_nama.addWidget(self.separator_4)

        self.value_nama = QLabel(self.centralwidget)
        self.value_nama.setObjectName(u"value_nama")

        self.layout_nama.addWidget(self.value_nama)

        self.layout_nama.setStretch(0, 2)
        self.layout_nama.setStretch(1, 2)
        self.layout_nama.setStretch(2, 15)

        self.layout_data.addLayout(self.layout_nama)

        self.layout_email = QHBoxLayout()
        self.layout_email.setObjectName(u"layout_email")
        self.label_email = QLabel(self.centralwidget)
        self.label_email.setObjectName(u"label_email")

        self.layout_email.addWidget(self.label_email)

        self.separator_3 = QLabel(self.centralwidget)
        self.separator_3.setObjectName(u"separator_3")

        self.layout_email.addWidget(self.separator_3)

        self.value_email = QLabel(self.centralwidget)
        self.value_email.setObjectName(u"value_email")

        self.layout_email.addWidget(self.value_email)

        self.layout_email.setStretch(0, 2)
        self.layout_email.setStretch(1, 2)
        self.layout_email.setStretch(2, 15)

        self.layout_data.addLayout(self.layout_email)

        self.layput_phone = QHBoxLayout()
        self.layput_phone.setObjectName(u"layput_phone")
        self.label_phone = QLabel(self.centralwidget)
        self.label_phone.setObjectName(u"label_phone")

        self.layput_phone.addWidget(self.label_phone)

        self.separator = QLabel(self.centralwidget)
        self.separator.setObjectName(u"separator")

        self.layput_phone.addWidget(self.separator)

        self.value_phone = QLabel(self.centralwidget)
        self.value_phone.setObjectName(u"value_phone")

        self.layput_phone.addWidget(self.value_phone)

        self.layput_phone.setStretch(0, 2)
        self.layput_phone.setStretch(1, 2)
        self.layput_phone.setStretch(2, 15)

        self.layout_data.addLayout(self.layput_phone)

        self.layout_saldo = QHBoxLayout()
        self.layout_saldo.setObjectName(u"layout_saldo")
        self.label_saldo = QLabel(self.centralwidget)
        self.label_saldo.setObjectName(u"label_saldo")

        self.layout_saldo.addWidget(self.label_saldo)

        self.separator_2 = QLabel(self.centralwidget)
        self.separator_2.setObjectName(u"separator_2")

        self.layout_saldo.addWidget(self.separator_2)

        self.value_saldo = QLabel(self.centralwidget)
        self.value_saldo.setObjectName(u"value_saldo")

        self.layout_saldo.addWidget(self.value_saldo)

        self.layout_saldo.setStretch(0, 2)
        self.layout_saldo.setStretch(1, 2)
        self.layout_saldo.setStretch(2, 15)

        self.layout_data.addLayout(self.layout_saldo)


        self.frame_main.addLayout(self.layout_data)

        self.frame_main.setStretch(0, 1)
        self.frame_main.setStretch(1, 1)

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

        Dashboard.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Dashboard)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 24))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        Dashboard.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Dashboard)
        self.statusbar.setObjectName(u"statusbar")
        Dashboard.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.navigateSettings)
        self.menuMenu.addAction(self.navigateRegister)
        self.menuMenu.addAction(self.navigateAddSaldo)

        self.retranslateUi(Dashboard)

        QMetaObject.connectSlotsByName(Dashboard)
    # setupUi

    def retranslateUi(self, Dashboard):
        Dashboard.setWindowTitle(QCoreApplication.translate("Dashboard", u"Dashboard", None))
        self.navigateSettings.setText(QCoreApplication.translate("Dashboard", u"Settings", None))
        self.navigateRegister.setText(QCoreApplication.translate("Dashboard", u"Register", None))
        self.navigateAddSaldo.setText(QCoreApplication.translate("Dashboard", u"Add Saldo", None))
        self.saldo.setText(QCoreApplication.translate("Dashboard", u"Biaya ", None))
        self.label.setText(QCoreApplication.translate("Dashboard", u":", None))
        self.value_biaya.setText(QCoreApplication.translate("Dashboard", u"0", None))
        self.label_sisa_saldo.setText(QCoreApplication.translate("Dashboard", u"Sisa Saldo ", None))
        self.label_2.setText(QCoreApplication.translate("Dashboard", u":", None))
        self.value_sisa_saldo.setText(QCoreApplication.translate("Dashboard", u"0", None))
        self.value_camera.setText("")
        self.label_nama.setText(QCoreApplication.translate("Dashboard", u"Nama", None))
        self.separator_4.setText(QCoreApplication.translate("Dashboard", u":", None))
        self.value_nama.setText("")
        self.label_email.setText(QCoreApplication.translate("Dashboard", u"Email", None))
        self.separator_3.setText(QCoreApplication.translate("Dashboard", u":", None))
        self.value_email.setText("")
        self.label_phone.setText(QCoreApplication.translate("Dashboard", u"Phone", None))
        self.separator.setText(QCoreApplication.translate("Dashboard", u":", None))
        self.value_phone.setText("")
        self.label_saldo.setText(QCoreApplication.translate("Dashboard", u"Saldo", None))
        self.separator_2.setText(QCoreApplication.translate("Dashboard", u":", None))
        self.value_saldo.setText("")
        self.status_internet.setText(QCoreApplication.translate("Dashboard", u"Price : 0", None))
        self.status_gate.setText(QCoreApplication.translate("Dashboard", u"Status : Online", None))
        self.status_cctv.setText(QCoreApplication.translate("Dashboard", u"CCTV : Connected", None))
        self.status_rfid.setText(QCoreApplication.translate("Dashboard", u"RFID : Connected", None))
        self.menuMenu.setTitle(QCoreApplication.translate("Dashboard", u"Menu", None))
    # retranslateUi

