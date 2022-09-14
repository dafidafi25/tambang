"""
ACR122u-A9
Mifare Classic 1K
pyscard (1.9.9)
"""
from operator import truediv
import time
import smartcard
from smartcard.util import toHexString

BLOCK_NUMBER = 0x00 #default
LOADKEY_A = [0xFF, 0x82, 0x00, 0x00, 0x06]
LOADKEY_B = [0xFF, 0x82, 0x00, 0x01, 0x06]
GET_UID = [0xFF,0xCA,0x00,0x00,0x04]
WRITE_16_BYTES = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, 0x10]
ATR_MIFARE_1k = [0x3B, 0x8F, 0x80, 0x01, 0x80, 0x4F, 0x0C, 0xA0, \
                0x00, 0x00, 0x03, 0x06, 0x03, 0x00, 0x01, 0x00, 0x00, \
                0x00 ,0x00, 0x6A] 
FORBIDDEN_BLOCKS = [0,3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63] 
#access trailer is forbidden to write by default

class SmartCard:
    def __init__(self):
        self.conn = None

    def isReaderDetected(self):
        self.reader = smartcard.System.readers()
        if len(self.reader) > 0:
            return True
        else:
            print("Not Detected")
            return False
    
    def connectReader(self):
        if(len(self.reader) > 0 ):
            try:
                self.conn = self.reader[0].createConnection()
                self.conn.connect()
                print("Reader Connected")
            except:
                print("Not Connected")
    
    def isNewCard(self):
        response = self.execute_command(ATR_MIFARE_1k)
        # try:
        #     response = self.execute_command(GET_UID)
        #     if self.check_validate(response):
        #         return True
            
        #     else:
        #         return False
        # except:
        #     return False
        
    
    def get_uid(self):
        response = self.execute_command()

    def check_validate(self,response):
        if response[1] == 144:
            return True
        return False
    
    def execute_command(self, command):
        try:
            response = self.conn.transmit(command)
            return response
        except:
            return []
        

if __name__=="__main__":
    SmartReader = SmartCard()
    while(1):
        isDetected = SmartReader.isReaderDetected()
        
        if not isDetected: 
            time.sleep(0.5)
            continue
        SmartReader.connectReader()

        # if not SmartReader.isNewCard() : 
        #     time.sleep(0.5)
        #     continue
        # print("Card Detected")
        time.sleep(0.5)
# get_uid(conn)
# # load_akey(conn)
# #write_block(conn)
# #read_sector(conn)
# # read_block(conn)

def get_uid(conn):
    response = execute_command(conn, GET_UID)
    if check_validate(response):
        return response[0]
        
    else:
        print("Error")
        return []

def make_conn():
    reader = smartcard.System.readers()
    if not reader:
        print("Reader Tidak Terdeteksi")
        return False
    else:
        conn =  reader[0].createConnection()
        conn.connect()
        print("Reader Terdeteksi "+str(reader))
        return conn

def execute_command(conn, command):
    response = conn.transmit(command)
    return response

def check_validate(response):
    if response[1] == 144:
        return True
    return False

def load_akey(conn, key):
    if len(key) == 6:
        key = [int(i) for i in key]
        for byte in key:
            if 0 <= byte <= 255:
                LOADKEY_A.append(byte)
            else:
                print("Número inválido: "+str(byte))
                return False
        response = execute_command(conn, LOADKEY_A)
        if check_validate(response):
            print("Proses Berhasil")
        else:
            print("Proses Gagal")
    else:
        print("Jumlah Key Harus 6 Byte")

def load_bkey(conn, key):
    if len(key) == 6:
        key = [int(i) for i in key]
        for byte in key:
            if 0 <= byte <= 255:
                LOADKEY_B.append(byte)
            else:
                print("Número inválido: "+str(byte))
                return False
        response = execute_command(conn, LOADKEY_B)
        if check_validate(response):
            print("Proses Berhasil")
        else:
            print("Proses Gagal")
    else:
        print("Jumlah Key Harus 6 Byte")

def read_sector(conn, sector):
    if 0 <= sector <= 15:
        time.sleep(2)
        for block in range(sector*4, sector*4+4):
            COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, block, 0x60, 0x00]
            execute_command(conn, COMMAND)
            response = execute_command(conn, [0xFF, 0xB0, 0x00, block, 0x10])
            if check_validate(response):
                print(toHexString(response[0]))
            else:
                print("Proses Error")
    else:
        print("Panjang Sector Maksimal 15")

def read_block(conn, BLOCK_NUMBER):
    if not 0 <= BLOCK_NUMBER <= 63:
        print("Nomor Block Tidak Valid")
        return
    print("Proses Block")
    time.sleep(2)
    COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, BLOCK_NUMBER, 0x60, 0x00]
    response = execute_command(conn, COMMAND)
    if check_validate(response):
        response = execute_command(conn,[0xFF, 0xB0, 0x00, BLOCK_NUMBER, 0x10])
        if check_validate(response):
            print(toHexString(response[0]))
        else:
            print("Block Error")
    else:
        print("Tidak Tervalidasi")


    
def write_block(conn, BLOCK_NUMBER, value_to_write):
    if not 0 <= BLOCK_NUMBER <= 63:
        print("Block Invalid")
        return
    if BLOCK_NUMBER in FORBIDDEN_BLOCKS:
        print("Forbidden Block Numbers")
        return
    WRITE_16_BYTES[3] = BLOCK_NUMBER
    list_value = []
    for value in value_to_write:
        list_value.append(int(hex(ord(value)),16))
    if len(list_value) == 16:
        for value in list_value:
            WRITE_16_BYTES.append(value)
        response = execute_command(conn, WRITE_16_BYTES)
        if check_validate(response):
            print("Block Write Success")
        else:
            print("Block Write Gagalt")
    else:
        print("Nilai Block Kurang dari 16")
        return
    

