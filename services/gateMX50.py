
import serial
from time import sleep
# from Enum import Response 
import re
import subprocess
import sys
import glob

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
        self.BAUD_RATE = BAUD_RATE
        self.USB_PORT = USB_PORT
        self.debug = debug
        self.serial = False
    
    def connectGate(self):
        self.serial = serial.Serial(self.USB_PORT,self.BAUD_RATE,timeout=0.05)
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
        print('buka')

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
        print(response)

        # if(self.debug):
        #     print(response,cmd)

        return response
    
    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyUSB*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/ttyUSB.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
                self.USB_PORT = port
            except Exception as err:
                print(err)
                return False
        return True

    # @staticmethod
    # def responseName(response):
    #     switcher = {
    #         Response.UNKNOWN: "Gerbang tidak menyentuh sensor limit",
    #         Response.DOWN_CMD_RECEIVED: "Perintah tutup diterima",
    #         Response.DOWN_LIMIT: "Gerbang tertutup",
    #         Response.UP_CMD_RECEIVED: "Perintah buka diterima",
    #         Response.UP_LIMIT: "Gerbang terbuka",
    #         Response.STOP_CMD_RECEIVED: "Perintah berhenti diterima"
    #     }


        # return switcher.get(response,"No Response")

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
    print(test.serial_ports())
    # # status_byte,status_string = test.getGateStatus()
    # test.closeGate()
    # sleep(2)
    # test.openGate()
    
