from PySide2.QtWidgets import QDialog
from view.AddForm import Ui_Dialog
from smartcard.util import toHexString
import requests
from utils.random_generators import hex_random_value

class DialogAddSaldo(QDialog):
    def __init__(self, rfid_service):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.rfid_service = rfid_service

        self.__initialize_button()
    
    def __initialize_button(self):
        self.ui.btn_scan_2.clicked.connect(self.__scan_rfid)
        self.ui.btn_confirm_2.clicked.connect(self.__add_saldo)
        pass

    def __scan_rfid(self):
        new_card_key = [0xff,0xff,0xff,0xff,0xff,0xff]
        if not self.ui.rfid_service.isNewCard(): 
            print("Card is not Detected")
            return False
        
        isLoaded = self.ui.rfid_service.loadAuthKey(new_card_key, 0)

        if not isLoaded: 
            print("Load Key Failed")
            return False
        response = self.ui.rfid_service.read_block(0,0)
        if len(response) ==  0: 
            print("Authentication Failed")
            return False
        
        self.ui.input_uid_2.setText(toHexString(response))
        return True

    def __add_saldo(self):
        saldo = self.get_saldo()
        uid = self.scan_rfid()
        generated_key = hex_random_value(6)

        url = 'http://0.0.0.0:6000/api/saldo'
        myobj = {
                 'saldo' : saldo,
                 'uid' : uid,
                 "key" : generated_key
                }

        x = requests.post(url, json = myobj)
        
        if x.status_code < 200 or x.status_code >299:
            return False
        
        isLoaded = self.ui.rfid_service.loadAuthKey([0xff,0xff,0xff,0xff,0xff,0xff], 1)
        
        if not isLoaded : return False
        print(generated_key)
        isSuccess = self.ui.rfid_service.set_wallet_sector( saldo,generated_key, 5, 1)

        if not isSuccess :return False
        return True
        pass

    def start(self):
        self.exec_()

    def __result_change_price():
        pass
