from ISAPI import isapiClient,response_parser,dateTimeConvert
from mySql import updateTable

ip = "192.168.1.64"
port = "80"
host = 'http://'+ip + ':'+ port
cam = isapiClient(host, 'admin', '-arngnennscfrer2')
db = updateTable('localhost','root','','tambang')
db.connectDatabase()

print(cam._check_session())
res = cam.getNumberPlates()
dbLatestTime = db.getPlateLatestTime()
plateResponse = response_parser(res)


try:
    listTest = plateResponse['Plates']['Plate']
    latestTime = dbLatestTime[0][0] if len(dbLatestTime) > 0 else 0
    print(latestTime)
except KeyError as err:
    print(err)
else:
    listTester = []
    for x in range(len(listTest)):
        # print(listTest[x]['captureTime'])
        timetest = dateTimeConvert(listTest[x]['captureTime'])
        if(timetest > latestTime):
            listTester.append((listTest[x]['plateNumber'],timetest))

    db.insertDataPlate(listTester)
    
        
    # db = updateTable('localhost','root','','tambang')
    # db.connectDatabase()
    # db.executeQuery("SELECT * FROM user")
    # db.fetchData()
    # print(db.getFetchData())



