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
AUTHENTICATION = []
GET_UID = [0xFF,0xCA,0x00,0x00,0x04]
WRITE_16_BYTES = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, 0x10]
ATR_MIFARE_1k = [0x3B, 0x8F, 0x80, 0x01, 0x80, 0x4F, 0x0C, 0xA0, \
                0x00, 0x00, 0x03, 0x06, 0x03, 0x00, 0x01, 0x00, 0x00, \
                0x00 ,0x00, 0x6A]
FORBIDDEN_BLOCKS = [0,3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63] 
#access trailer is forbidden to write by default
authA = [0x00,0x00,0x00,0x00,0x00,0x00]
authB = [0xff,0xff,0xff,0xff,0xff,0xff]

class SmartCard:
    def __init__(self):
        self.conn = None

    def isReaderDetected(self):
        self.reader = smartcard.System.readers()
        if len(self.reader) > 0:
            return True
        else:
            self.reader = None
            return False
    
    def isNewCard(self):
        if(len(self.reader) > 0 ):
            try:
                self.conn = self.reader[0].createConnection()
                self.conn.connect()
                return True
            except: return False
        else: return False
        
    
    def get_uid(self):
        response = self.execute_command()

    def check_validate(self,response):
        if response[1] == 144:
            return True
        return False
    
    def execute_command(self, command):
        try:
            print(toHexString(response))
            response = self.conn.transmit(command)
            print(toHexString(response))
            return response
        except:
            return []

    def setWalletSector(self,saldo,sector = 2):
        block = sector
        sector_trailer = block +3
        wallet_format,auth_format = self.getValueBlockFormat(saldo,block)
        print(wallet_format)
        print(auth_format)
        # self.write_block(block,16,1,wallet_format)
        # self.changeForbiddenBlocks(sector_trailer,16,1,auth_format)

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

    def changeForbiddenBlocks(self,sector):
        print(FORBIDDEN_BLOCKS[sector])
    
    def load_akey(self, key):
        command = []
        command.extend(LOADKEY_A)
        if len(key) == 6:
            key = [int(i) for i in key]
            for byte in key:
                if 0 <= byte <= 255:
                    command.append(byte)
                else:
                    print("Key Invalid "+str(byte))
                    return False
            response = self.execute_command(command)
            if self.check_validate(response):
                return True
            else:
                return False
        else:
            return False

    def load_bkey(self, key):
        command = []
        command.extend(LOADKEY_B)
        if len(key) == 6:
            key = [int(i) for i in key]
            for byte in key:
                if 0 <= byte <= 255:
                    command.append(byte)
                else:
                    print("Nomor Invalif "+str(byte))
                    return False
            response = self.execute_command(command)
            if self.check_validate(response):
                return True
            else:
                return False
        else:
            return False
    
    def read_block(self, BLOCK_NUMBER, key, type = 0):
        if not 0 <= BLOCK_NUMBER <= 63:
            print("Nomor Block Tidak Valid")
            return False
        if type == 0:
            self.load_akey(key)
        if type == 1:
            self.load_bkey(key)
        print("Proses Block")
        COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, BLOCK_NUMBER, 0x60, 0x00]
        response = self.execute_command(COMMAND)
        if self.check_validate(response):
            response = self.execute_command([0xFF, 0xB0, 0x00, BLOCK_NUMBER, 0x10])
            if self.check_validate(response):
               
                print(toHexString(response[0]))
                return response[0]
            else:
                # print("Block Error")
                return []
        else:
            # print("Tidak Tervalidasi")
            return []
        
    def write_block(self, BLOCK_NUMBER, value_to_write, key, type = 0):
        if not 0 <= BLOCK_NUMBER <= 63:
            print("Block Invalid")
            return
        if BLOCK_NUMBER in FORBIDDEN_BLOCKS:
            print("Forbidden Block Numbers")
            return
        
        if type == 0:
            self.load_akey(key)
        if type == 1:
            self.load_bkey(key)
        WRITE_16_BYTES[3] = BLOCK_NUMBER
        command = WRITE_16_BYTES
        print(toHexString(command))

        
        # if len(value_to_write) == 16:
        #     command.extend(value_to_write)
        #     response = self.execute_command(command)
        #     if self.check_validate(response):
        #         print("Block Write Success")
        #     else:
        #         print("Block Write Gagal")
        # else:
        #     print("Nilai Block Kurang dari 16")
        #     return

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
    


if __name__=="__main__":
    tag_write = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x10,0x11,0x12,0x13,0x14,0x15]
    SmartReader = SmartCard()
    while(1):
        isDetected = SmartReader.isReaderDetected()
        
        if not isDetected: continue
        if not SmartReader.isNewCard() : continue
        try:
            SmartReader.load_akey(authB)
            # SmartReader.write_block(10, tag_write, authA, type=0)
            # value = SmartReader.read_block(0x01, authA, 0)
            # print(value)
        except Exception as err:
            print(err)
        finally:
            time.sleep(0.5)
        
# get_uid(conn)
# # load_akey(conn)
# #write_block(conn)
# #read_sector(conn)
# # read_block(conn)