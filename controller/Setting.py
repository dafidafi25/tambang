from PySide2.QtWidgets import QDialog
from view.SettingsForm import Ui_Dialog

class DialogSetting(QDialog):
    def __init__(self, service_gate):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__service_gate = service_gate

        self.__initialize_button()
    
    def __initialize_button(self):
        self.ui.btn_open_gate.clicked.connect(self.__open_gate)
        self.ui.btn_close_gate.clicked.connect(self.__close_gate)

    def __change_price():
        pass

    def __open_gate(self):
        self.__service_gate.openGate()
        pass

    def __close_gate(self):
        self.__service_gate.closeGate()
        pass
       
    def start(self):
        self.exec_()

    def __result_change_price():
        pass
