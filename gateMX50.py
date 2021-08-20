

class gateProcess:
    def __init__(self):
        self.gateStatus = False
    
    def getGateStatus(self):
        return self.gateStatus

    def openGate(self):
        self.gateStatus = True

    def closeGate(self):
        self.gateStatus = False