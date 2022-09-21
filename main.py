from sys import argv, exit


from PySide2.QtWidgets import QApplication

from controller.Dashboard import DashboardController


class Main():
    def __init__(self):
        super().__init__()
        print("Masok")
        self.ui = DashboardController()
        print("Masok")

    def start(self):
        self.ui.start()
        

if __name__ == '__main__':
    app = QApplication(argv)
    main = Main()
    main.start()
    exit(app.exec_())