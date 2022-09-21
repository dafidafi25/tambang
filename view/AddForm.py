# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addForm.ui'
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
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layou_curr_saldo_2 = QHBoxLayout()
        self.layou_curr_saldo_2.setObjectName(u"layou_curr_saldo_2")
        self.label_curr_saldo_2 = QLabel(Dialog)
        self.label_curr_saldo_2.setObjectName(u"label_curr_saldo_2")

        self.layou_curr_saldo_2.addWidget(self.label_curr_saldo_2)

        self.separator_6 = QLabel(Dialog)
        self.separator_6.setObjectName(u"separator_6")

        self.layou_curr_saldo_2.addWidget(self.separator_6)

        self.value_curr_saldo_2 = QLabel(Dialog)
        self.value_curr_saldo_2.setObjectName(u"value_curr_saldo_2")

        self.layou_curr_saldo_2.addWidget(self.value_curr_saldo_2)

        self.layou_curr_saldo_2.setStretch(0, 5)
        self.layou_curr_saldo_2.setStretch(1, 1)
        self.layou_curr_saldo_2.setStretch(2, 12)

        self.verticalLayout.addLayout(self.layou_curr_saldo_2)

        self.layout_add_saldo_2 = QHBoxLayout()
        self.layout_add_saldo_2.setObjectName(u"layout_add_saldo_2")
        self.label_add_saldo_2 = QLabel(Dialog)
        self.label_add_saldo_2.setObjectName(u"label_add_saldo_2")

        self.layout_add_saldo_2.addWidget(self.label_add_saldo_2)

        self.separator_5 = QLabel(Dialog)
        self.separator_5.setObjectName(u"separator_5")

        self.layout_add_saldo_2.addWidget(self.separator_5)

        self.Input_price_2 = QLineEdit(Dialog)
        self.Input_price_2.setObjectName(u"Input_price_2")

        self.layout_add_saldo_2.addWidget(self.Input_price_2)

        self.layout_add_saldo_2.setStretch(0, 5)
        self.layout_add_saldo_2.setStretch(1, 1)
        self.layout_add_saldo_2.setStretch(2, 12)

        self.verticalLayout.addLayout(self.layout_add_saldo_2)

        self.layout_sum_2 = QHBoxLayout()
        self.layout_sum_2.setObjectName(u"layout_sum_2")
        self.label_sum_2 = QLabel(Dialog)
        self.label_sum_2.setObjectName(u"label_sum_2")

        self.layout_sum_2.addWidget(self.label_sum_2)

        self.separator_4 = QLabel(Dialog)
        self.separator_4.setObjectName(u"separator_4")

        self.layout_sum_2.addWidget(self.separator_4)

        self.value_sum_2 = QLabel(Dialog)
        self.value_sum_2.setObjectName(u"value_sum_2")

        self.layout_sum_2.addWidget(self.value_sum_2)

        self.layout_sum_2.setStretch(0, 5)
        self.layout_sum_2.setStretch(1, 1)
        self.layout_sum_2.setStretch(2, 12)

        self.verticalLayout.addLayout(self.layout_sum_2)

        self.layout_btn_2 = QHBoxLayout()
        self.layout_btn_2.setObjectName(u"layout_btn_2")
        self.btn_scan_2 = QPushButton(Dialog)
        self.btn_scan_2.setObjectName(u"btn_scan_2")

        self.layout_btn_2.addWidget(self.btn_scan_2)

        self.btn_confirm_2 = QPushButton(Dialog)
        self.btn_confirm_2.setObjectName(u"btn_confirm_2")

        self.layout_btn_2.addWidget(self.btn_confirm_2)


        self.verticalLayout.addLayout(self.layout_btn_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_curr_saldo_2.setText(QCoreApplication.translate("Dialog", u"Saldo Sekarang", None))
        self.separator_6.setText(QCoreApplication.translate("Dialog", u":", None))
        self.value_curr_saldo_2.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_add_saldo_2.setText(QCoreApplication.translate("Dialog", u"Tambah Saldo", None))
        self.separator_5.setText(QCoreApplication.translate("Dialog", u":", None))
        self.label_sum_2.setText(QCoreApplication.translate("Dialog", u"Total", None))
        self.separator_4.setText(QCoreApplication.translate("Dialog", u":", None))
        self.value_sum_2.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.btn_scan_2.setText(QCoreApplication.translate("Dialog", u"Scan", None))
        self.btn_confirm_2.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
    # retranslateUi

