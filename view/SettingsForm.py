# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsForm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 200)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_open_gate = QPushButton(Dialog)
        self.btn_open_gate.setObjectName(u"btn_open_gate")

        self.verticalLayout_2.addWidget(self.btn_open_gate)

        self.btn_close_gate = QPushButton(Dialog)
        self.btn_close_gate.setObjectName(u"btn_close_gate")

        self.verticalLayout_2.addWidget(self.btn_close_gate)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.input_price = QLineEdit(Dialog)
        self.input_price.setObjectName(u"input_price")
        self.input_price.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.input_price)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_save = QPushButton(Dialog)
        self.btn_save.setObjectName(u"btn_save")

        self.horizontalLayout.addWidget(self.btn_save)

        self.btn_cancel = QPushButton(Dialog)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.horizontalLayout.addWidget(self.btn_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(2, 5)

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.btn_open_gate.setText(QCoreApplication.translate("Dialog", u"Buka Gerbang", None))
        self.btn_close_gate.setText(QCoreApplication.translate("Dialog", u"Tutup Gerbang", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Ubah Harga : ", None))
        self.input_price.setPlaceholderText(QCoreApplication.translate("Dialog", u"50000", None))
        self.btn_save.setText(QCoreApplication.translate("Dialog", u"Simpan", None))
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Batal", None))
    # retranslateUi

