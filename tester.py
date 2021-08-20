from ISAPI import Client,response_parser,dateTimeConvert
from mySql import updateTable

ip = "192.168.1.64"
port = "80"
host = 'http://'+ip + ':'+ port
cam = Client(host, 'admin', '-arngnennscfrer2')
db = updateTable('localhost','root','','tambang')
db.connectDatabase()

print(cam._check_session())
res = cam.getNumberPlates()

plateResponse = response_parser(res)


try:
    listTest = plateResponse['Plates']['Plate']
except KeyError as err:
    print(err)
else:
    records_to_insert = [(4, 'HP Pavilion Power', 1999, '2019-01-11'),
                         (5, 'MSI WS75 9TL-496', 5799, '2019-02-27'),
                         (6, 'Microsoft Surface', 2330, '2019-07-23')]
    listTester = []
    for x in range(len(listTest)):
        # print(listTest[x]['captureTime'])
        timetest = dateTimeConvert(listTest[x]['captureTime'])
        listTester.append((listTest[x]['plateNumber'],timetest))
    # print(listTester)
    db.insertDataPlate(listTester)
    db.commit()
    
        
    # db = updateTable('localhost','root','','tambang')
    # db.connectDatabase()
    # db.executeQuery("SELECT * FROM user")
    # db.fetchData()
    # print(db.getFetchData())



