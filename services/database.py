import mysql.connector
from datetime import datetime,timedelta
import json
from authentication import AESCipher

import datetime;

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

class databases:
  def __init__(self,host,user,password,database):
    self.host = host
    self.user = user
    self.password = password
    self.database = database
    self.mycursor = ""
    
  
  def connectDatabase(self):
    self.mydb = mysql.connector.connect(
    host=self.host,
    user=self.user,
    password=self.password,
    database=self.database
    )
    self.mycursor = self.mydb.cursor()

  def executeQuery(self,query,val = None):
    # print(query)
    try:
      assert val != None
    except AssertionError:
      try:
        self.mycursor.execute(query)
      except mysql.connector.Error as err:
        print(err)
    else:
      try:
        assert type(val) == tuple
      except AssertionError:
        self.mycursor.executemany(query,val)
      except mysql.connector.errors as err:
        print(err)

      else:
        self.mycursor.execute(query,val)
    
  def fetchData(self):
    self.myresult = self.mycursor.fetchall()
    return self.myresult
  
  def insertDataPlate(self,value):
    query = "insert into hikvision (hikvision_plat,hikvision_time) values(%s,%s)"
    # value = ("w1234df", value)
    self.executeQuery(query,value)
    self.commit(self)
  
  def getPlateLatestTime(self):
    query = "Select hikvision_time from hikvision order by hikvision_time desc limit 1"
    self.executeQuery(query)
    data = self.fetchData()
    data = data[0][0] if len(data) > 0 else None
    return data
  
  def isUserExist(self,username):
    query = "SELECT * from card WHERE username LIKE %s"
    self.executeQuery(query,(username,))

    row = self.fetchData()

    if len(row) >0:
      return True
    else:
      return False
  
  def isUidExist(self,uid):
      query = "SELECT * from card WHERE uid LIKE %s"
      self.executeQuery(query,(AESCipher(key2).encrypt(uid),))
      row = self.fetchData()

      if len(row) > 0:
        return True
      else:
        return False

  def getUserByUid(self,uid):
      query = "SELECT * from card WHERE UID = %s"
      self.executeQuery(query,(AESCipher(key2).encrypt(uid),))
      row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
      data = self.fetchData()
      json_data = []
      for result in data:
        json_data.append(dict(zip(row_headers,result)))
      if len(json_data) > 0:
        json_data[0]['UID'] = AESCipher(key2).decrypt(json_data[0]['UID']).decode("utf-8")
        json_data[0]['saldo'] = AESCipher(key1).decrypt(json_data[0]['saldo']).decode("utf-8")
        json_data[0]['keyA'] = AESCipher(json_data[0]['saldo']).decrypt(json_data[0]['keyA'])
      return json_data


  def register(self,uid,key,saldo,username,email,phone):
    query = "INSERT INTO card (UID,keyA,saldo,username,email,phone) values(%s,%s,%s,%s,%s,%s)"
    value = (uid,key,saldo,username,email,phone)
   
    if self.isUserExist(username) == True or self.isUidExist(AESCipher(key2).encrypt(uid)) == True:
      return False
    else:
      value = (AESCipher(key2).encrypt(uid),AESCipher(str(saldo)).encrypt(key),AESCipher(key1).encrypt(str(saldo)),username,email,phone)
      self.executeQuery(query,value)
      self.fetchData()
      self.commit()
      return True
  
  def updateSaldo(self,key_access,uid,newSaldo):
    query = "UPDATE card SET keyA= %s ,saldo = %s WHERE UID = %s"
    val = (AESCipher(str(key_access)).encrypt(newSaldo),newSaldo,uid)
    self.executeQuery(query,val)
    test = self.fetchData()
    self.commit()
    
    return True


  def getUserPage(self,page,per_page):
    query = "SELECT * from card"

    self.executeQuery(query)
    row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
    data = self.fetchData()
    json_data=[]

    for result in data:
      json_data.append(dict(zip(row_headers,result)))
    return json_data
    
  def getGateStatus(self):
    query = "SELECT * from gate"

    self.executeQuery(query)
    row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
    data = self.fetchData()
    json_data=[]

    for result in data:
      json_data.append(dict(zip(row_headers,result)))
    return json_data
  
  def setGate(self, gate, id):
    query = ("UPDATE gate \
              SET gate = %s \
              WHERE id = %s ")
    value = (gate,id)
    result =  self.executeQuery(query,value)
    self.commit()
    return result

  def setGateStatus(self, gate, id):
    query = ("UPDATE gate \
              SET gate_status = %s \
              WHERE id = %s ")
    value = (gate,id)
    result =  self.executeQuery(query,value)
    self.commit()
    return result
  
  def setPrice(self,price,id):
    query = ("UPDATE gate \
              SET price = %s \
              WHERE id = %s ")
    value = (price,id)
    self.executeQuery(query,value)
    self.commit()
  
  def getDevicePrice(self):
      query = "SELECT * FROM gate"
      self.executeQuery(query)
      row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
      data = self.fetchData()
      json_data=[]
      for result in data:
        json_data.append(dict(zip(row_headers,result)))
      return json_data


  def insertDataTransaksi(self,card_id,plate_number,status,price):
    created_at = datetime.datetime.now()
    query = "insert into transaksi (created_at,card_id,plate_number,status,price) values(%s,%s,%s,%s,%s)"
    value = (str(created_at)[0:19],card_id,plate_number,status,price)
    
    self.executeQuery(query,value)
    return self.commit(True)
  
  def getListTransaksi(self):
    query = "select * from transaksi order by id desc"
    self.executeQuery(query)
    row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
    data = self.fetchData()
    json_data=[]
    for result in data:
      json_data.append(dict(zip(row_headers,result)))
    return json_data

  def mergeLicenseTable(self,value_id,value_time):
    query = ("UPDATE hikvision \
              SET transaksi_id = %s \
              WHERE transaksi_id IS NULL \
              AND hikvision_time BETWEEN %s AND %s")
    value_time1 = value_time - timedelta(minutes = 3)
    value_time2 = value_time + timedelta(minutes = 1)
    value = (value_id,value_time1,value_time2)
    print(value)
    self.executeQuery(query,value)
    self.commit()
    

  def commit(self,id=None):
    self.mydb.commit()
    if id == None:
      print(self.mycursor.rowcount, "was inserted.")
    if id == True:
      print("1 record inserted, ID:", self.mycursor.lastrowid)
      return self.mycursor.lastrowid

if __name__ == "__main__":
 
  db = databases('localhost','root','root','tambangku')
  db.connectDatabase()
  index_test = 0
  data_test = "text" + str(index_test)

  db.register('',data_test,index_test,data_test,data_test,data_test)
  # result = db.getUserByUid(AESCipher(key2).encrypt(data_test))
  # print(result)

  # print(db.getPlateLatestTime())
  # # print(db.getPlateLatestTime())
  
