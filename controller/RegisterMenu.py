from PySide2.QtWidgets import QDialog
from view.RegisteForm import Ui_Dialog
from smartcard.util import toHexString
import requests
from utils.random_generators import hex_random_value

class DialogRegister(QDialog):
    def __init__(self, rfid_service):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.rfid_service = rfid_service

        self.__initialize_button()
    
    def __initialize_button(self):
        self.ui.btn_register_2.clicked.connect(self.__register)
        self.ui.btn_scan_2.clicked.connect(self.__scan_rfid)
        pass

    def __register(self):
        email = self.ui.input_email_2.text()
        phone = self.ui.input_phone_2.text()
        saldo = self.ui.input_saldo_2.text()
        uid = self.ui.input_uid_2.text()
        username = self.ui.input_username_2.text()
        generated_key = hex_random_value(6)

        url = 'http://0.0.0.0:6000/api/register'
        myobj = {'username': username,
                 'email' : email,
                 'phone' : phone,
                 'saldo' : saldo,
                 'uid' : uid,
                 'key' : toHexString(generated_key)
                }

        x = requests.post(url, json = myobj)

        
        if x.status_code < 200 or x.status_code >299:
            return False
        
        print(email,phone,saldo,uid,username)
        print("Coba register")


        if self.ui.rfid_service.isNewCard():
            isLoaded = self.ui.rfid_service.loadAuthKey([0xff,0xff,0xff,0xff,0xff,0xff], 1)
            try:
                self.ui.rfid_service.get_uid()
                self.ui.rfid_service.loadAuthKey([0xff,0xff,0xff,0xff,0xff,0xff], type = 1)
                isSuccess = self.ui.rfid_service.set_wallet_sector( saldo,generated_key, 5, 1)
                print(isSuccess)
            
            except Exception as err:
                print(err)
            print(isLoaded)

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

    def __close_gate(self):
        pass
    
    def start(self):
        self.exec_()

    def __result_change_price():
        pass
