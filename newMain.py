from ISAPI import isapiClient,response_parser,dateTimeConvert
from time import sleep
from smartCard2 import DetectReader,smartCard
from gateMX50 import gate
from mySql import databases
from Enum import GateSetting
from smartcard.util import *
from Authentication import AESCipher

SECTOR = [4*0,4*1,4*2,4*3,4*4,4*5,4*6,4*7,4*8,4*9,4*10,4*11,4*12,4*13,4*14,4*15]

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

BAUD_RATE = 0
USB_PORT = ""
GATE_ADDRESS = 0
listSmartReader = []
smartReader = []


settings = []
with open('setting.txt') as f:
    settings = f.readlines()




for setting in settings:
    menuName = setting[0:setting.index("=")]
    
    if menuName == GateSetting.BAUD_RATE.value:

        BAUD_RATE =setting[setting.index("=")+1: len(setting)-1]

    if menuName == GateSetting.USB_PORT.value:
        USB_PORT = setting[setting.index("=")+1: len(setting)-1]
        
    if menuName == GateSetting.GATE_ADDRESS.value:
        GATE_ADDRESS = setting[setting.index("=")+1: len(setting)]


gateControl = gate(GATE_ADDRESS=int(GATE_ADDRESS),BAUD_RATE= BAUD_RATE,USB_PORT=USB_PORT)



while True:
    while len(listSmartReader) == 0:
        print("Trying to detect reader")
        listSmartReader = DetectReader()
        sleep(0.5)

    while len(listSmartReader) != 0:
       
        db = databases('localhost','root','root','tambangku')
        db.connectDatabase()

        try :
            smartReader = smartCard()
            deviceConnected = smartReader.connect()
            assert deviceConnected, "Device Not Connected"

        except AssertionError as msg:
            print(msg)

        except Exception as e:
            print(e)
            listSmartReader= []

        if deviceConnected:
            gateControlStatus = gateControl.getGateStatus()
            cardValue = []
            if(len(gateControlStatus) > 0 ):
                status = [x for x in gateControlStatus]
                status = True if status[1] == 12  else False
            else:
                status = False
            
            if(smartReader.isNewCard()):
                
                if(status):
                    cardValue = smartReader.readCard()
                
                else:
                    print("Gate")
                
                if cardValue:
                    if db.isUidExist(AESCipher(key2).encrypt(cardValue)):
                        result = db.getUserByUid(AESCipher(key2).encrypt(cardValue))

                        saldo = result[0]['saldo']
                        id = result[0]['id']
                        uid = result[0]['UID']
                        price = db.getDevicePrice()[0]['price']

                    
                        
                        if saldo > int(price):
                            newSaldo = saldo -int(price)
                            keyA = result[0]['keyA']
                            key_access = AESCipher(str(saldo)).decrypt(keyA).decode('utf-8')
                            wallet_format,key_access = smartReader.getValueBlockFormat(newSaldo,SECTOR[10]+1)
                            gateControl.openGate()
                            db.insertDataTransaksi(id,"",1,price)
                            print(newSaldo)
                            db.updateSaldo(AESCipher(str(newSaldo)).encrypt(toHexString(key_access)),uid,newSaldo)
                            smartReader.setWalletSector(newSaldo,10)
                            
                            
                    cardValue = False

            
            # else:
            #     if gateControlStatus == 0x05:
            #         gateControl.copenGate()

        #Pengecekan Kembali Reader Terhubung
        listSmartReader = DetectReader()
        sleep(0.5)

    sleep(0.5)

