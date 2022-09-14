
import serial
from time import sleep
from Enum import Response 



###Command###
CHECK_GATE = 0x00
OPEN_GATE = 0x03
CLOSE_GATE = 0x05
STOP_GATE = 0x01
###Command###
FIXED_DATA = 0x00

class gate:
    def __init__(self,GATE_ADDRESS,BAUD_RATE,USB_PORT,debug = False):
        self.GATE_ADDRESS = GATE_ADDRESS
        self.debug = debug
        self.serial = serial.Serial(USB_PORT,BAUD_RATE,timeout=0.05)
        self.serial.reset_input_buffer()
    
    def getGateStatus(self):
        cmd = [self.GATE_ADDRESS,CHECK_GATE,FIXED_DATA]
        verify_bits = self.verifyBits(cmd)     
        cmd.append(verify_bits)
        return self.sendCmd(cmd)

    def openGate(self):
        cmd = [self.GATE_ADDRESS,OPEN_GATE,FIXED_DATA]

        verify_bits = self.verifyBits(cmd)     
        cmd.append(verify_bits)

        return self.sendCmd(cmd)

    def closeGate(self):
        cmd = [self.GATE_ADDRESS,CLOSE_GATE,FIXED_DATA]

        verify_bits = self.verifyBits(cmd)     
        cmd.append(verify_bits)

        return self.sendCmd(cmd)

    def sendCmd(self,cmd):
        self.serial.write(cmd)
        response = []
        
        response = (self.serial.read(4))

        # if(self.debug):
        #     print(response,cmd)

        return response

    @staticmethod
    def responseName(response):
        switcher = {
            Response.UNKNOWN: "Gerbang tidak menyentuh sensor limit",
            Response.DOWN_CMD_RECEIVED: "Perintah tutup diterima",
            Response.DOWN_LIMIT: "Gerbang tertutup",
            Response.UP_CMD_RECEIVED: "Perintah buka diterima",
            Response.UP_LIMIT: "Gerbang terbuka",
            Response.STOP_CMD_RECEIVED: "Perintah berhenti diterima"
        }


        return switcher.get(response,"No Response")

    @staticmethod 
    def verifyBits(cmd):
        verify_bits = 0x00
        for bytes in cmd:
            verify_bits = verify_bits ^ bytes
            
        return verify_bits


if __name__ == "__main__":
    BAUD_RATE = 9600
    USB_PORT = "/dev/ttyUSB0"
    GATE_ADDRESS = 0x05
    test = gate(GATE_ADDRESS=GATE_ADDRESS,BAUD_RATE= BAUD_RATE,USB_PORT=USB_PORT)
    # status_byte,status_string = test.getGateStatus()
    test.closeGate()
    sleep(2)
    test.openGate()
    

