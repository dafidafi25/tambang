from time import sleep
from smartcard.System import readers
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
from smartcard.util import *
debug = False



##list of basic command
sReaderFirmware = [0xff,0x71,0x00,0x00,0x00]
authA = [0x00,0x00,0x00,0x00,0x00,0x00]
authB = [0xff,0xff,0xff,0xff,0xff,0xff]

class smartCard:
    def __init__(self):
        self.reader = readers()
        self.connected = False

    def connect(self):
        self.connection = self.reader[0].createConnection()
        self.connection.connect()
        return smartCard.isConnected(self)

    def isConnected(self):
        data,sw1,sw2 = self.connection.transmit(sReaderFirmware)
        if sw1 == 0x90:
            return True
        else :
            return False

    def isNewCard(self): #Initiate so device can start read TAG
        # start1 = [0xff, 0x71, 0x13, 0x06, 0x00]  # set SAM communication to contactless
        start2 = [0xff, 0x71, 0x10, 0x00, 0x00]  # reset SAM communication
        if smartCard.sendCmd(start2,self) == 0x90:
            return True
        else:
            return False

    def readCard(self):
        smartCard.setTempAuth(0,authA,self)
        smartCard.setTempAuth(1,authB,self)
        if smartCard.readBlock(0,16,1,self):
            return True
        else:
            return False
        
 
    def setTempAuth(storeNumb,keyNumb,self): # Load & Set Authentication Key to Reader
        authKey = [0xFF, 0x82 ,0x00]
        authKey.append(storeNumb)
        authKey.append(0x06)
        authKey+= keyNumb
        if smartCard.sendCmd(authKey,self):
            return True
        else:
            return False

    def mifareAuth(blockNumber,keyType,self):
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
        if smartCard.sendCmd(auth,self) == 0x90:
            return True
        else:
            return False
    
    def readBlock(blockNumber,length,keyType,self):
        if smartCard.mifareAuth(blockNumber,keyType,self):
            readCmd = [0xff,0xb0,0x00]
            readCmd.append(blockNumber)
            readCmd.append(length)
            if smartCard.sendCmd(readCmd,self) == 0x90:
                return True
            else:
                return False
        else:
            return False
    
    def sendCmd(cmd,self): #Send Command to Reader
        if debug:
            print("Data dikirim ==>  " + toHexString(cmd))
        data, sw1, sw2 = self.connection.transmit(cmd)
        if debug:
            print ("response : %x %x" % (sw1, sw2))
        if len(data) > 0:
            if debug:
                print("response Data = ",toHexString(data))
            
        return sw1


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
    deviceConnected = False
    test = DetectReader()
 