import enum

###RESPONSE GATE###
class Response (enum.Enum):
    UNKNOWN = 0x00
    UP_LIMIT = 0x09
    DOWN_LIMIT = 0x0c
    STOP_CMD_RECEIVED = 0x01
    UP_CMD_RECEIVED = 0x03
    DOWN_CMD_RECEIVED = 0x05
###RESPONSE GATE###

### GATE SETTING ###

class GateSetting (enum.Enum):
    BAUD_RATE = "BAUD_RATE"
    USB_PORT = "USB_PORT"
    GATE_ADDRESS = "GATE_ADDRESS"


