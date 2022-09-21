"""
ACR122u-A9
Mifare Classic 1K
pyscard (1.9.9)
"""
from ast import Pass
from operator import truediv
import time
from smartcard.System import readers
from smartcard.util import toHexString

### DEFAULT VALUE ###
sReaderFirmware = [0xff,0x00,0x48,0x00,0x00]
BLOCK_NUMBER = 0x00 
KEY_TYPE = 0x60 # 0x60 = type A 0x61 = type B
KEY_NUMBER = 0 # 2 location, 0 for A 1 for B
### DEFAULT VALUE ###

### Command ACR 122u ###
LOADKEY_A = [0xFF, 0x82, 0x00, 0x00, 0x06]
LOADKEY_B = [0xFF, 0x82, 0x00, 0x01, 0x06]
AUTHENTICATION = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x00, BLOCK_NUMBER, KEY_TYPE, KEY_NUMBER]
GET_UID = [0xFF,0xCA,0x00,0x00,0x04]
WRITE_16_BYTES = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, 0x10]

### Command ACR 122u ###


FORBIDDEN_BLOCKS = [0,3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63] # Sector Trailer Block for Each Sector
#access trailer is forbidden to write by default

### Default Authentication by Mifare Docs
authB = [0x00,0x00,0x00,0x00,0x00,0x00]
authA = [0xff,0xff,0xff,0xff,0xff,0xff]
### Default Authentication by Mifare Docs

class SmartCard:
    def __init__(self):
        self.conn = None

    def isReaderDetected(self):
        self.reader = readers()
        if len(self.reader) > 0:
            return True
        else:
            self.reader = None
            return False
    
    def isNewCardDetected(self):
        if(len(self.reader) > 0 ):
            try:
                self.conn = self.reader[0].createConnection()
                self.conn.connect()
                # print('connected')
                return True
            except Exception as err:
                # print('disconnected')
                return False
        else: 
            # print('no detected')
            return False
    
    def diconnect(self):
        if self.conn is not  None : self.conn.disconnect()
        
    def get_uid(self):
        response = self.execute_command(GET_UID)
        if self.check_validate(response):
            return response[0]
        else:
            return False

    def check_validate(self,response):
        if response[1] == 144:
            return True
        return False
    
    def execute_command(self, command):
        response = self.conn.transmit(command)
        return response
        

    def setWalletSector(self,saldo, random_key,block = 4, type = 0):
        if not block >= 3 : raise(f'Dont Write sector 0 !')
        if block in FORBIDDEN_BLOCKS : raise(f'Cant set Sector trailer to Value Block ')
        sector_trailer = None
        temp = block
        while sector_trailer is None: 
            sector_trailer = temp if temp in FORBIDDEN_BLOCKS  else None
            temp += 1 
        # print(f'Sector Trailer Detected: {sector_trailer}')
        wallet_format,auth_format = self.getValueBlockFormat(saldo,block, random_key)
        # print(f'Wallet block format : {toHexString(wallet_format)} \nAuth Format : {toHexString(auth_format)}')
        if  isinstance(wallet_format,bool) : return (False,False)
        if isinstance(auth_format,bool)  : return (False,False)

        write_response = self.write_block(block,wallet_format, type)
        sector_response = self.changeForbiddenBlocks(sector_trailer,auth_format,type)
        return (write_response, sector_response)

    def getValueBlockFormat(self,saldo,RESERVED_BLOCK, random_key):
        if len(random_key) is not 6 : return False, False
        BASIC_AUTH_KEY = [0xff,0xff,0xff,0xff,0xff,0xff]
        BASIC_ACCESS_BITS = [0xff,0x07,0x80]
        VALUE_BLOCK = []
        AUTH_BLOCK = []
        BYTES = saldo.to_bytes(4,'little')
        INVERTED_BYTES = self.invertBytes(BYTES)
        INVERTED_RESERVED_BLOCK =  RESERVED_BLOCK ^ 0xff

        VALUE_BLOCK.extend(BYTES)
        VALUE_BLOCK.extend(INVERTED_BYTES)
        VALUE_BLOCK.extend(BYTES)
        VALUE_BLOCK.append(RESERVED_BLOCK)
        VALUE_BLOCK.append(INVERTED_RESERVED_BLOCK)
        VALUE_BLOCK.append(RESERVED_BLOCK)
        VALUE_BLOCK.append(INVERTED_RESERVED_BLOCK)

        AUTH_BLOCK.extend(random_key)
        AUTH_BLOCK.extend(BASIC_ACCESS_BITS)
        AUTH_BLOCK.append(0x69)
        AUTH_BLOCK.extend(BASIC_AUTH_KEY)
        print(toHexString(AUTH_BLOCK))

        return VALUE_BLOCK, AUTH_BLOCK

    def changeForbiddenBlocks(self,BLOCK_NUMBER, value_to_write, type = 0):
        COMMAND = []
        if type == 0:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x60, 0x00]
        if type == 1:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x61, 0x01]
        
        response = self.execute_command(COMMAND)
        if self.check_validate(response):
            write_command = []
            write_command = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, 0x10]
            write_command.extend(value_to_write)
            response = self.conn.transmit(write_command)
            if self.check_validate(response):
                return response[0]
            else:
                return []
        else:
            return []
    
    def load_akey(self, key):
        if len(key) == 6:
            command = []
            command.extend(LOADKEY_A)
            command.extend(key)
            response = self.execute_command(command)
            if self.check_validate(response):
                return True
            else:
                return False
        else:
            return False

    def load_bkey(self, key):
        if len(key) == 6:
            command = []
            command.extend(LOADKEY_B)
            command.extend(key)
            response = self.execute_command(command)
            if self.check_validate(response):
                return True
            else:
                return False
        else:
            raise False
    
    def read_block(self, BLOCK_NUMBER, type = 0):
        if not 0 <= BLOCK_NUMBER <= 63:
            return False
        if type == 0:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x60, 0x00]
        if type == 1:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x61, 0x01]

        response = self.execute_command(COMMAND)
        if self.check_validate(response):
            COMMAND = [0xFF, 0xB0, 0x00, BLOCK_NUMBER, 0x10]
            response = self.execute_command(COMMAND)
            if self.check_validate(response):
                return response[0]
            else:
                return []
        else:
            return []
        
    def write_block(self, BLOCK_NUMBER, value_to_write, type = 0):
        if not 0 <= BLOCK_NUMBER <= 63:
                return False
        if BLOCK_NUMBER in FORBIDDEN_BLOCKS: raise f'Dont Write to sector trailer directly'
        if type == 0:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x60, 0x00]
        if type == 1:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x61, 0x01]
        response = self.execute_command(COMMAND)
        if self.check_validate(response):
            write_command = []
            write_command = [0xFF, 0xD6, 0x00, BLOCK_NUMBER, 0x10]
            write_command.extend(value_to_write)
            response = self.conn.transmit(write_command)
            if self.check_validate(response):
                return response[0]
            else:
                return []
        else:
            return []
    
    def read_value_block(self, BLOCK_NUMBER, type = 0):
        if not 0 <= BLOCK_NUMBER <= 63:
            return False
        if type == 0:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x60, 0x00]
        if type == 1:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x61, 0x01]

        response = self.execute_command(COMMAND)
        if self.check_validate(response):
            COMMAND = [0xFF, 0xB1, 0x00, BLOCK_NUMBER, 0x04]
            response = self.execute_command(COMMAND)
            if self.check_validate(response):
                return response[0]
            else:
                raise f'Non Valid Response with command \nCommand : {toHexString(COMMAND)}'
        else:
            raise f'Non Valid Response with command \nCommand : {toHexString(COMMAND)}'
    
    def increment_value_block(self, BLOCK_NUMBER, value, type = 0):
        if not 0 <= BLOCK_NUMBER <= 63:
            return False
        if type == 0:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x60, 0x00]
        if type == 1:
            COMMAND = [0xFF, 0x88, 0x00, BLOCK_NUMBER, 0x61, 0x01]
        
        response = self.execute_command(COMMAND)
        if self.check_validate(response):
            COMMAND = [0xFF, 0xD7, 0x00, BLOCK_NUMBER, 0x05, 0x01]
            value = value.to_bytes(4,'big')
            COMMAND.extend(value)
            print(toHexString(COMMAND))
            response = self.execute_command(COMMAND)
            if self.check_validate(response):
                return response[0]
            else:
                raise f'Non Valid Response with command \nCommand : {toHexString(COMMAND)}'
        else:
            raise f'Non Valid Response with command \nCommand : {toHexString(COMMAND)}'

    

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
        
        if not SmartReader.isNewCardDetected(): 
            time.sleep(0.5)
            continue
        
        try:
            response = SmartReader.get_uid()
            isAuth = SmartReader.load_bkey([0xff,0xff,0xff,0xff,0xff,0xff])

            if isAuth:
                result = SmartReader.read_block(0,0)
                print(result)
                # value = SmartReader.read_value_block(5,1)
                
        except Exception as err:
            print(err)
        
        # SmartReader.diconnect()
        time.sleep(0.5)

class TAG_EXCEPTION(Exception):
    def __init__(self, message):
        self.message = message

        super().__init__(message)

    def __str__(self):
        return self.message
        
# get_uid(conn)
# # load_akey(conn)
# #write_block(conn)
# #read_sector(conn)
# # read_block(conn)