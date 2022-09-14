# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RegisteForm.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.layput_username = QHBoxLayout()
        self.layput_username.setObjectName(u"layput_username")
        self.label_username = QLabel(self.centralwidget)
        self.label_username.setObjectName(u"label_username")

        self.layput_username.addWidget(self.label_username)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.layput_username.addWidget(self.label_6)

        self.input_username = QLineEdit(self.centralwidget)
        self.input_username.setObjectName(u"input_username")

        self.layput_username.addWidget(self.input_username)

        self.layput_username.setStretch(0, 2)
        self.layput_username.setStretch(1, 1)
        self.layput_username.setStretch(2, 9)

        self.verticalLayout.addLayout(self.layput_username)

        self.layout_email = QHBoxLayout()
        self.layout_email.setObjectName(u"layout_email")
        self.label_email = QLabel(self.centralwidget)
        self.label_email.setObjectName(u"label_email")

        self.layout_email.addWidget(self.label_email)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.layout_email.addWidget(self.label_8)

        self.input_email = QLineEdit(self.centralwidget)
        self.input_email.setObjectName(u"input_email")

        self.layout_email.addWidget(self.input_email)

        self.layout_email.setStretch(0, 2)
        self.layout_email.setStretch(1, 1)
        self.layout_email.setStretch(2, 9)

        self.verticalLayout.addLayout(self.layout_email)

        self.layout_phone = QHBoxLayout()
        self.layout_phone.setObjectName(u"layout_phone")
        self.label_phone = QLabel(self.centralwidget)
        self.label_phone.setObjectName(u"label_phone")

        self.layout_phone.addWidget(self.label_phone)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.layout_phone.addWidget(self.label_9)

        self.input_phone = QLineEdit(self.centralwidget)
        self.input_phone.setObjectName(u"input_phone")

        self.layout_phone.addWidget(self.input_phone)

        self.layout_phone.setStretch(0, 2)
        self.layout_phone.setStretch(1, 1)
        self.layout_phone.setStretch(2, 9)

        self.verticalLayout.addLayout(self.layout_phone)

        self.layout_saldo = QHBoxLayout()
        self.layout_saldo.setObjectName(u"layout_saldo")
        self.label_saldo = QLabel(self.centralwidget)
        self.label_saldo.setObjectName(u"label_saldo")

        self.layout_saldo.addWidget(self.label_saldo)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.layout_saldo.addWidget(self.label_10)

        self.input_saldo = QLineEdit(self.centralwidget)
        self.input_saldo.setObjectName(u"input_saldo")

        self.layout_saldo.addWidget(self.input_saldo)

        self.layout_saldo.setStretch(0, 2)
        self.layout_saldo.setStretch(1, 1)
        self.layout_saldo.setStretch(2, 9)

        self.verticalLayout.addLayout(self.layout_saldo)

        self.layou_uid = QHBoxLayout()
        self.layou_uid.setObjectName(u"layou_uid")
        self.label_uid = QLabel(self.centralwidget)
        self.label_uid.setObjectName(u"label_uid")

        self.layou_uid.addWidget(self.label_uid)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.layou_uid.addWidget(self.label_11)

        self.input_uid = QLineEdit(self.centralwidget)
        self.input_uid.setObjectName(u"input_uid")

        self.layou_uid.addWidget(self.input_uid)

        self.layou_uid.setStretch(0, 2)
        self.layou_uid.setStretch(1, 1)
        self.layou_uid.setStretch(2, 9)

        self.verticalLayout.addLayout(self.layou_uid)

        self.layout_action = QHBoxLayout()
        self.layout_action.setObjectName(u"layout_action")
        self.btn_scan = QPushButton(self.centralwidget)
        self.btn_scan.setObjectName(u"btn_scan")

        self.layout_action.addWidget(self.btn_scan)

        self.btn_register = QPushButton(self.centralwidget)
        self.btn_register.setObjectName(u"btn_register")

        self.layout_action.addWidget(self.btn_register)


        self.verticalLayout.addLayout(self.layout_action)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Form Pendaftaran", None))
        self.label_username.setText(QCoreApplication.translate("MainWindow", u"Username ", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_email.setText(QCoreApplication.translate("MainWindow", u"Email ", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_phone.setText(QCoreApplication.translate("MainWindow", u"Phone", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_saldo.setText(QCoreApplication.translate("MainWindow", u"Saldo", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.label_uid.setText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u":", None))
        self.btn_scan.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.btn_register.setText(QCoreApplication.translate("MainWindow", u"Daftar", None))
    # retranslateUi

