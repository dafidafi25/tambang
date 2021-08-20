from ISAPI import isapiClient,response_parser,dateTimeConvert
from time import sleep
from smartCard2 import DetectReader,smartCard
from gateMX50 import gateProcess
from mySql import updateTable

deviceConnected = False

while len(DetectReader()) == 0:
    print("Trying to detect reader")
    sleep(1)
print("reader Detected")
smartReader = smartCard()
gateControl = gateProcess()
db = updateTable('localhost','root','','tambang')
db.connectDatabase()


try :
    deviceConnected = smartReader.connect()
    assert deviceConnected, " Device Not Connected"

except AssertionError as msg:
    print(msg)
    deviceConnected = False

else :
    print("Device Connected")

while deviceConnected:
    try :
        assert smartReader.isConnected() ,"Device not Connected"

    except AssertionError as msg:
        print(msg)
        sleep(1)
        continue
    else :
        try:
            assert smartReader.isNewCard(), "Waiting for New Card"
        
        except AssertionError as msg:
            print(msg)
            gateControl.closeGate()
            sleep(1)
            continue

        else :
            try:
                assert smartReader.readCard(),"There is No Card"
            
            except AssertionError as msg:
                print(msg)
                sleep(1)
                continue

            else:
                try:
                    ip = "192.168.1.64"
                    port = "80"
                    host = 'http://'+ip + ':'+ port
                    cam = isapiClient(host, 'admin', '-arngnennscfrer2')
                    assert gateControl.getGateStatus() == False,"Gate Still Openning"
                except AssertionError as msg:
                    print(msg)
                    sleep(1)
                    continue
                else:
                    waktu_transaksi = cam.systemTime()
                    get_id = db.insertDataTransaksi(waktu_transaksi)
                    db.updateLicenseTable(get_id,waktu_transaksi)
                    gateControl.openGate()
    
    sleep(1)


        
        


# cam = Client('http://192.168.1.64:80', 'admin', '-arngnennscfrer2')
# print(cam._check_session())