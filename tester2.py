from smartcard.System import readers
from smartcard.util import toHexString


#Starting connection
device = readers()
connection = device[0].createConnection()
connection.connect()
print('device connected')



authA = '00 00 00 00 00 00'
authB = 'FF FF FF FF FF FF'



def init(): #Initiate so device can start read TAG
    # start1 = 'ff 71 14 00 00'  # set SAM communication to contactless
    # start1 = bytearray.fromhex(start1)
    # sendCmd(start1)
    start2 = 'ff 71 10 00 00'  # reset SAM communication
    start2 = bytearray.fromhex(start2)
    sendCmd(start2)

def setTempAuth(storeNumb,keyNumb): # Load & Set Authentication Key to Reader
    authKey = 'FF 82 00'
    authKey = bytes.fromhex(authKey)
    authKey = authKey + bytes([storeNumb])
    authKey = authKey + bytes([6])
    authKey = authKey + bytes.fromhex(keyNumb)
    sendCmd(authKey)

def sendCmd(cmd): #Send Command to Reader
    # cmd = bytearray.fromhex(cmd)
    cmd = list(cmd)
    print("Data dikirim ==>  " + toHexString(cmd))
    data, sw1, sw2 = connection.transmit(cmd)
    print ("response : %x %x" % (sw1, sw2))
    if len(data) > 0:
        print('response data : ' + toHexString(data))
    return sw1

#Authentication to TAG keyTypeA = 0 || keyTypeB = 1
def mifareAuth(blockNumber,keyType):
    auth = 'ff 86 00 00 05 01 00'
    auth = bytearray.fromhex(auth)
    auth = auth + bytes([blockNumber])
    if keyType == 0 :
        auth = auth + bytes([0x60])
        auth = auth + bytes([0])
    elif keyType == 1:
        auth = auth + bytes([0x61])
        auth = auth + bytes([1])
    else:
        return 'Auth Not Valid'
    # print(auth)
    return sendCmd(auth)

def readBlock(blockNumber,length,keyType):
    validity = mifareAuth(blockNumber,keyType)

    if  validity == 144:
        readCmd = 'ff b0 00'
        readCmd = bytearray.fromhex(readCmd)
        readCmd += bytes([blockNumber])
        readCmd += bytes([length])
        sendCmd(readCmd)

def writeBlock():
    print("wawa")

init()



readBlock(blockNumber=0, length=16, keyType =10)