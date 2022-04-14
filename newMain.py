from ISAPI import isapiClient,response_parser,dateTimeConvert
from time import sleep
from smartCard2 import DetectReader,smartCard
from gateMX50 import gateProcess
from mySql import updateTable

listSmartReader = []
smartReader = []

while True:
    while len(listSmartReader) == 0:
        print("Trying to detect reader")
        listSmartReader = DetectReader()
        sleep(0.5)

    while len(listSmartReader) != 0:
        # print("Reader Detected : " + str(smartReader[0]))
        db = updateTable('localhost','root','root','tambangku')
        db.connectDatabase()

        try :
            smartReader = smartCard()
            deviceConnected = smartReader.connect()
            assert deviceConnected, "Device Not Connected"

        except AssertionError as msg:
            print(msg)

        except Exception as e:
            print(e)
            listSmartReader= []

        if deviceConnected:
            if(smartReader.isNewCard()):
                smartReader.readCard()

        #Pengecekan Kembali Reader Terhubung
        listSmartReader = DetectReader()
        sleep(0.5)



    sleep(0.5)

