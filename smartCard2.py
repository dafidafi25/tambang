from asyncore import write
from time import sleep
from smartcard.System import readers
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
from smartcard.util import *
debug = False

##list of basic command
sReaderFirmware = [0xff,0x71,0x00,0x00,0x00]
BLOCK_NUMBER = 0x00 #default
LOADKEY_A = [0xFF, 0x82, 0x00, 0x00, 0x06]
GET_UID = [0xFF,0xCA,0x00,0x00,0x04]
WRITE_16_BYTES = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, 0x10]
FORBIDDEN_BLOCKS = [0,3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63] 
authA = [0x00,0x00,0x00,0x00,0x00,0x00]
authB = [0xff,0xff,0xff,0xff,0xff,0xff]

SECTOR = [4*0,4*1,4*2,4*3,4*4,4*5,4*6,4*7,4*8,4*9,4*10,4*11,4*12,4*13,4*14,4*15]

class smartCard:
    def __init__(self):
        self.reader = readers()

    def connect(self):
        self.connection = self.reader[0].createConnection()
        self.connection.connect()

        return self.isConnected()

    def isConnected(self):
        data,sw1,sw2 = self.connection.transmit(sReaderFirmware)
        if sw1 == 0x90:
            return True
        else :
            return False

    def isNewCard(self): #Initiate so device can start read TAG
        # start1 = [0xff, 0x71, 0x13, 0x06, 0x00]  # set SAM communication to contactless
        start2 = [0xff, 0x71, 0x10, 0x00, 0x00]  # reset SAM communication
        sw1 ,data = self.sendCmd(start2)
        if sw1 == 0x90:
            return True
        else:
            return False

    def readCard(self):
        self.setTempAuth(0,authA)
        self.setTempAuth(1,authB)
        sw1,data = self.readBlock(0,16,1)
        if sw1 ==0x90:
            return data
        else:
            return False
        
 
    def setTempAuth(self,storeNumb,keyNumb): # Load & Set Authentication Key to Reader
        authKey = [0xFF, 0x82 ,0x00]
        authKey.append(storeNumb)
        authKey.append(0x06)
        authKey.extend(keyNumb)
        sw1 ,data = self.sendCmd(authKey)
        if sw1 == 0x90:
            return True
        else:
            return False

    def mifareAuth(self,blockNumber,keyType):
        auth = [0xFF, 0x86 ,0x00, 0x00, 0x05, 0x01, 0x00]
        auth += [blockNumber]
        if keyType == 0 :
            auth += [0x60]
            auth += [0]
        elif keyType == 1:
            auth += [0x61]
            auth += [1]
        else:
            return 'Auth Not Valid'
        sw1 ,data = self.sendCmd(auth)
        if sw1 == 0x90:
            return True
        else:
            return False
    
    def readBlock(self,blockNumber,length,keyType):
        if self.mifareAuth(blockNumber,keyType):
            readCmd = [0xff,0xb0,0x00]
            readCmd.append(blockNumber)
            readCmd.append(length)
            sw1 ,data = self.sendCmd(readCmd)
            
            if sw1 == 0x90:
                return  (sw1 ,toHexString(data))
            else:
                return (False,None)
        else:
            return (False,None)


    def writeBlock(self,blockNumber,length,keyType,data):
        if self.mifareAuth(blockNumber,keyType):
            writeCmd = [0xff,0xd6,0x00]
            writeCmd.append(blockNumber)
            writeCmd.append(length)
            writeCmd.extend(data)
            sw1 ,data = self.sendCmd(writeCmd)

            if sw1 == 0x90:
                return  (sw1 ,toHexString(data))
            else:
                return (False,None)

    def valueBlock(self,saldo,sector = 2):
        block = sector * 4
        RESERVED_BLOCK = block + 1
        VALUE_BLOCK = []
        BYTES = saldo.to_bytes(4,'big')
        INVERTED_BYTES = self.invertBytes(BYTES)
        INVERTED_RESERVED_BLOCK =  RESERVED_BLOCK ^ 0xff

        VALUE_BLOCK.extend(BYTES)
        VALUE_BLOCK.extend(INVERTED_BYTES)
        VALUE_BLOCK.extend(BYTES)
        VALUE_BLOCK.append(RESERVED_BLOCK)
        VALUE_BLOCK.append(INVERTED_RESERVED_BLOCK)
        VALUE_BLOCK.append(RESERVED_BLOCK)
        VALUE_BLOCK.append(INVERTED_RESERVED_BLOCK)
       
        print(VALUE_BLOCK)


    def increment(self,sector,value,key_access):
        block = sector * 4
        RESERVED_BLOCK = block + 1
        SECTOR_TRAILER = block + 3

        #keperluan reset
        wallet_format, auth_format = self.getValueBlockFormat(50000,RESERVED_BLOCK)
        self.writeBlock(block,16,1,wallet_format)
        #keperluan reset

        # value = value.to_bytes(4,'big')
        # self.setTempAuth(0,bytearray.fromhex(key_access[0:17]))
        # self.mifareAuth(block,0)

        # cmd = [0xff,0xD7,0x00,block,0x05,0x01]
        # cmd.extend(value)
        # sw1,data = self.sendCmd(cmd)

        data = self.readValueBlock(sector,key_access)
        print(toHexString(data))
      
    
    def decrement(self,sector,value,key_access,auth_type = 0):
        
        print(value)
        block = sector
        RESERVED_BLOCK = block + 1
        SECTOR_TRAILER = block + 3
        value = value.to_bytes(4,'big')
        # generated_key = bytearray.fromhex(key_access[0:17])
        self.setTempAuth(auth_type,key_access)
        self.mifareAuth(block,auth_type)

        cmd = [0xff,0xD7,0x00,block,0x05,0x02]
        cmd.extend(value)
        print(toHexString(cmd))

        test = self.sendCmd(cmd)
        print(test)

        # data = self.readValueBlock(sector,key_access)
        # print(toHexString(data))

       
    def readValueBlock(self,sector,key_access):
        block = sector * 4
        RESERVED_BLOCK = block + 1
        SECTOR_TRAILER = block + 3
        cmd = [0xff,0xB1,0x00,block,4]
        sw1,data = self.sendCmd(cmd)
        
        if sw1 == 0x90:
            return data
        else:
            return False
        

    
    
    def sendCmd(self,cmd): #Send Command to Reader
        if debug:
            print("Data dikirim ==>  " + toHexString(cmd))
    
        data, sw1, sw2 = self.connection.transmit(cmd)
        
        if debug:
            print ("response : %x %x" % (sw1, sw2))
        if len(data) > 0:
            if debug:
                print("response Data = ",toHexString(data))
            
            
        return sw1,data
    
    def setWalletSector(self,saldo,sector = 2):
        block = sector
        sector_trailer = block +3
        wallet_format,auth_format = self.getValueBlockFormat(saldo,block)
        self.writeBlock(block,16,1,wallet_format)
        self.writeBlock(sector_trailer,16,1,auth_format)



    def getValueBlockFormat(self,saldo,RESERVED_BLOCK):
        BASIC_AUTH_KEY = [0xff,0xff,0xff,0xff,0xff,0xff]
        BASIC_ACCESS_BITS = [0xff,0x07,0x80]
        VALUE_BLOCK = []
        AUTH_BLOCK = []
        BYTES = saldo.to_bytes(4,'big')
        INVERTED_BYTES = self.invertBytes(BYTES)
        INVERTED_RESERVED_BLOCK =  RESERVED_BLOCK ^ 0xff

        VALUE_BLOCK.extend(BYTES)
        VALUE_BLOCK.extend(INVERTED_BYTES)
        VALUE_BLOCK.extend(BYTES)
        VALUE_BLOCK.append(RESERVED_BLOCK)
        VALUE_BLOCK.append(INVERTED_RESERVED_BLOCK)
        VALUE_BLOCK.append(RESERVED_BLOCK)
        VALUE_BLOCK.append(INVERTED_RESERVED_BLOCK)

        AUTH_BLOCK.append(0xff)
        AUTH_BLOCK.append(0xff)
        AUTH_BLOCK.extend(BYTES)
        AUTH_BLOCK.extend(BASIC_ACCESS_BITS)
        AUTH_BLOCK.append(0x69)
        AUTH_BLOCK.extend(BASIC_AUTH_KEY)

        return VALUE_BLOCK, AUTH_BLOCK
        

    @staticmethod
    def invertBytes(BYTES):
        INVERTED_BYTES = []
        for byte in BYTES:
            INVERTED_BYTES.append(byte^0xff)
        return bytes(INVERTED_BYTES)

    @staticmethod
    def accessBitsChecker(accessbits):
        for i in range(len(accessbits)):
            if i == 0:
                Ic2,Ic1 = (accessbits[i] >> 4, accessbits[i] & 0xf)
            if i == 1:
                c1,Ic3 = (accessbits[i] >>4, accessbits[i] & 0xf)
            if i == 2:
                c3,c2 = (accessbits[i] >>4, accessbits[i] & 0xf)
        valid = True
        valid = False if Ic2 ^ 0xf != c2 else valid
        valid = False if Ic1 ^ 0xf != c1 else valid
        valid = False if Ic3 ^ 0xf != c3 else valid

        return valid
    

class PrintObserver(ReaderObserver):
    def __init__(self):
        self.cards = []
    
    def update(self, observable, actions):
        (addedreaders, removedreaders) = actions 
        
        for card in addedreaders:
            if card not in self.cards:
                self.cards +=[card]
                print("Smartcard Detected: ", card)
                

        for card in removedreaders:
            print("-Removed: ", card)
            if card in self.cards:
                self.cards.remove(card)
    
    def getReader(self):
        return self.cards

def DetectReader():
    readermonitor = ReaderMonitor()
    print(readermonitor)
    readerobserver = PrintObserver()
    readermonitor.addObserver(readerobserver)
    sleep(1)
    # readermonitor.deleteObserver(readerobserver)
    return readerobserver.getReader()

if __name__ == "__main__":
    # sReaderFirmware = [0xff,0x71,0x00,0x00,0x00]
    # authA = [0x00,0x00,0x00,0x00,0x00,0x00]
    # authB = [0xff,0xff,0xff,0xff,0xff,0xff]
    # wallet_auth = [0xff,0xff,0x00,0x00,0xc3,0x50]

    # block = 0

    test_smartcard = smartCard()
    test_smartcard.connect()
    # while 1:
    #     if test_smartcard.isNewCard() :
    #         print('kartu baru')

    #     sleep(1)  
        

    # test_smartcard.setTempAuth(1,authB)
    # test_smartcard.setWalletSector(50000,SECTOR[11])
    # # block,key = test_smartcard.getValueBlockFormat(50000,SECTOR[11]+1)
    # test_smartcard.decrement(SECTOR[11],81,authB,1)
    # print(test_smartcard.readBlock(SECTOR[11],16,1))
    # print(test_smartcard.readBlock(SECTOR[11]+1,16,1))
    # print(test_smartcard.readBlock(SECTOR[11]+2,16,1))
    # print(test_smartcard.readBlock(SECTOR[11]+3,16,1))
    # print(valid)