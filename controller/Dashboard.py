from view.Dashboard import Ui_MainWindow
from PySide2.QtWidgets import QMainWindow

from PySide2.QtGui import QPixmap, QColor


class DashboardController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui  = Ui_MainWindow()

        self.ui.setupUi(self)
        self.ui.value_sisa_saldo.setText("0")
        self.ui.biaya.setText("0")

        grey = QPixmap(500,401)
        grey.fill(QColor('darkgray'))

        self.ui.label.setPixmap(grey)

    def start(self):
        self.show()