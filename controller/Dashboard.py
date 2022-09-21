from view.Dashboard import Ui_Dashboard
from PySide2.QtWidgets import QMainWindow

from PySide2.QtGui import QPixmap, QColor

from .thread.GateThread import GateThread
from .thread.HikvisionThread import HikvisionThread
from .thread.SmartCardThread import SmartCardThread


class DashboardController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui  = Ui_Dashboard()

        self.ui.setupUi(self)

        grey = QPixmap(500,401)
        grey.fill(QColor('darkgray'))

        self.ui.value_camera.setPixmap(grey)
    
    def __card_signal():
        pass

    def __gate_status():
        pass

    def __smart_card_status():
        pass

    def __price_status():
        pass

    def start(self):
        self.show()