# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsMenu.ui'
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
from PySide2.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 100)
        MainWindow.setMinimumSize(QSize(400, 100))
        MainWindow.setMaximumSize(QSize(400, 100))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelInput = QLabel(self.centralwidget)
        self.labelInput.setObjectName(u"labelInput")
        self.labelInput.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.labelInput)

        self.frame_action = QFrame(self.centralwidget)
        self.frame_action.setObjectName(u"frame_action")
        self.frame_action.setFrameShape(QFrame.StyledPanel)
        self.frame_action.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_action)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.input_cash = QLineEdit(self.frame_action)
        self.input_cash.setObjectName(u"input_cash")

        self.horizontalLayout.addWidget(self.input_cash)

        self.btn_confirm = QPushButton(self.frame_action)
        self.btn_confirm.setObjectName(u"btn_confirm")

        self.horizontalLayout.addWidget(self.btn_confirm)


        self.verticalLayout.addWidget(self.frame_action)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelInput.setText(QCoreApplication.translate("MainWindow", u"Ganti Biaya", None))
        self.btn_confirm.setText(QCoreApplication.translate("MainWindow", u"Simpan", None))
    # retranslateUi

