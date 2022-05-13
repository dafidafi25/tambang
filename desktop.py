import sys

from PySide2.QtGui import QIcon
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication, QMainWindow

from main_ui import Ui_MainWindow

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Akses Kontrol")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QApplication(sys.argv)
window = Window()

window.show()

sys.exit(app.exec_())