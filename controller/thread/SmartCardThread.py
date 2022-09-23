from curses.ascii import US
from sqlite3 import connect
import string
from time import sleep
from PySide2.QtCore import QThread, Signal
from services.smartCardAcs import SmartCard
from serial import SerialException
from utils.random_generators import hex_random_value
from smartcard.util import toHexString

class SmartCardThread(QThread):
    connect_signal = Signal(bool)
    card_signal = Signal(type)

    def __init__(self):
        super().__init__()
        self.__smart_card_service = SmartCard()
        self.read_mode = 1
    
    def isConnect(self):
        return self.__smart_card_service.isReaderDetected()
    
    def isNewCard(self):
        return self.__smart_card_service.isNewCardDetected()
    
    def loadAuthKey(self, key, type):
        isLoaded = False
        if type is 0 :
            isLoaded = self.__smart_card_service.load_akey(key)
        elif type is 1 :
            isLoaded = self.__smart_card_service.load_bkey(key)
        
        if isLoaded:
            return True
        else:
            return False
    
    def read_block(self, BLOCK_NUMBER, type):
        response = self.__smart_card_service.read_block(BLOCK_NUMBER, type)
        if len(response) > 0 :
            return response
        else : return []

    def write_block(self, BLOCK_NUMBER, type):
        response = self.__smart_card_service.write_block(BLOCK_NUMBER, type)
        if len(response) > 0 :
            print(response)
        else : print("gagal")
    
    def read_value_block(self, BLOCK_NUMBER, type):
        response = self.__smart_card_service.read_value_block(BLOCK_NUMBER, type)
        if len(response) > 0 :
            print(response)
        else : print("gagal")
    

    def set_wallet_sector(self, saldo,random_key, BLOCK_NUMBER, type):
        write_response, sector_response = self.__smart_card_service.setWalletSector(int(saldo),random_key, BLOCK_NUMBER, type)

        if isinstance(write_response, bool):
            print("Random Key Must be 6 Bytes")
            return False
        
        if isinstance(sector_response, bool):
            print("Random Key Must be 6 Bytes")
            return False

        if len(write_response) > 0:
            print("Set Wallet Gagal")
            return False
        
        if len(sector_response) > 0:
            print("Set Wallet Gagal")
            return False
        
        print("Set Wallet Berhasil")
        return True
    
    def increment_block():
        pass

    def decrement_block():
        pass

    def run(self):
        while(1):
            if not self.isConnect():
                
                self.connect_signal.emit(False)
            else:    
                self.connect_signal.emit(True)
                
                if self.read_mode == 1:
                    if self.isNewCard():
                        try:
                            self.__smart_card_service.get_uid()
                            self.loadAuthKey([0xff,0xff,0xff,0xff,0xff,0xff], type = 1)
                            tag = self.read_block(0,1)
                            if len(tag) > 0 : self.card_signal.emit(toHexString(tag))
                        
                        except Exception as err:
                            print(err)

                        

                self.__smart_card_service.diconnect()
            sleep(0.5)


