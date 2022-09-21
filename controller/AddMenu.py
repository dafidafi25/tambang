from PySide2.QtWidgets import QDialog
from view.AddForm import Ui_Dialog

class DialogAddSaldo(QDialog):
    def __init__(self,rfid_service):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.rfid_service = rfid_service
    
    def __initialize_button(self):
        pass

    def __change_price():
        pass

    def __open_gate(self):
        pass

    def __close_gate(self):
        pass
    
    def closeEvent(self, event):
        self.ui.rfid_service.read_mode = 1

    def start(self):
        self.exec_()

    def __result_change_price():
        pass
