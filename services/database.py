from asyncio import constants
from time import sleep
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
    self.mycursor = self.mydb.cursor(buffered=True)

  def executeQuery(self,query,val = None):
    # print(query)
    if type(val) == tuple:
      self.mycursor.executemany(query,val)
    elif val != None:
      self.mycursor.execute(query,val)
    else:
      self.mycursor.execute(query)
    
  def fetchData(self):
    self.myresult = self.mycursor.fetchall()
    return self.myresult

  def isUserExist(self,username):
    self.mycursor = self.mydb.cursor(buffered=True)
    query = "SELECT * from card WHERE username LIKE %s"
    self.executeQuery(query,(username,))

    row = self.fetchData()

    self.mycursor.close()
    if len(row) >0:
      return True
    else:
      return False
  
  def isUidExist(self,uid):
      self.mycursor = self.mydb.cursor(buffered=True)
      query = "SELECT * from card WHERE uid LIKE %s"
      self.executeQuery(query,(AESCipher(key2).encrypt(uid),))
      row = self.fetchData()
      self.mycursor.close()
      if len(row) > 0:
        return True
      else:
        return False

  def getUserByUid(self,uid):
      self.mycursor = self.mydb.cursor(buffered=True)
      query = "SELECT * from card WHERE UID = %s"
      self.executeQuery(query,(AESCipher(key2).encrypt(uid),))
      row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
      data = self.fetchData()
      json_data = []

      self.mycursor.close()
      for result in data:
        json_data.append(dict(zip(row_headers,result)))

      if len(json_data) > 0:
        json_data[0]['UID'] = AESCipher(key2).decrypt(json_data[0]['UID']).decode("utf-8")
        json_data[0]['saldo'] = AESCipher(key1).decrypt(json_data[0]['saldo']).decode("utf-8")
        json_data[0]['keyA'] = AESCipher(json_data[0]['saldo']).decrypt(json_data[0]['keyA'])
      return json_data


  def register(self,uid,key,saldo,username,email,phone):
    self.mycursor = self.mydb.cursor(buffered=True)
    query = "INSERT INTO card (UID,keyA,saldo,username,email,phone) values(%s,%s,%s,%s,%s,%s)"
    value = (uid,key,saldo,username,email,phone)
   
    if self.isUserExist(username) == True or self.isUidExist(AESCipher(key2).encrypt(uid)) == True:
      self.mycursor.close()
      return False
    else:
      value = (AESCipher(key2).encrypt(uid),AESCipher(str(saldo)).encrypt(key),AESCipher(key1).encrypt(str(saldo)),username,email,phone)
      self.executeQuery(query,value)
      self.fetchData()
      self.commit()
      self.mycursor.close()
      return True
  
  def updateSaldo(self,key_access,uid,newSaldo):
    self.mycursor = self.mydb.cursor(buffered=True)
    query = "UPDATE card SET keyA= %s ,saldo = %s WHERE UID = %s"
    val = (AESCipher(str(key_access)).encrypt(newSaldo),newSaldo,uid)
    self.executeQuery(query,val)
    test = self.fetchData()
    self.commit()
    self.mycursor.close()
    return True


  def getUserPage(self,page,per_page):
    self.mycursor = self.mydb.cursor(buffered=True)
    query = "SELECT * from card"

    self.executeQuery(query)
    row_headers=[x[0] for x in self.mycursor.description] #this will extract row headers
    data = self.fetchData()
    json_data=[]
    self.mycursor.close()
    for result in data:
      json_data.append(dict(zip(row_headers,result)))
    return json_data
    
  def getGateStatus(self):
    query = "SELECT * from gate where id = 1"
    gate_cursor = self.mydb.cursor(buffered=True)
    gate_cursor.execute(query)
    if len(gate_cursor.description) >  0 :
      row_headers=[x[0] for x in gate_cursor.description] #this will extract row headers
      data = gate_cursor.fetchone()
      data_arr = []
      data_arr.append(data)
      gate_cursor.close()
      if data is not None:
        json_data=[]
        for result in data_arr:
          json_data.append(dict(zip(row_headers,result)))
        return json_data
      else:
        return[]
        
    else:
      gate_cursor.close()
      return []
  def setGate(self, gate, id):
    set_gate_cursor = self.mydb.cursor(buffered=True)
    print(f'Gate : {gate} with id : {id}')
    query = ("UPDATE gate \
              SET gate = %s \
              WHERE id = %s ")
    value = (gate,id)
  
    try:
      set_gate_cursor.execute(query,value)
      self.mydb.commit()
    except Exception as err:
      print(err)
    finally:
      sleep(0.5)
      set_gate_cursor.close()
      return True 

  def setGateStatus(self, gate, id):
    self.mycursor = self.mydb.cursor(buffered=True)
    query = ("UPDATE gate \
              SET gate_status = %s \
              WHERE id = %s ")
    value = (gate,id,)
    result =  self.executeQuery(query,value)
    self.commit()
    self.mycursor.close()
    return result
  
  def setPrice(self,price,id):
    self.mycursor = self.mydb.cursor(buffered=True)
    query = ("UPDATE gate \
              SET price = %s \
              WHERE id = %s ")
    value = (price,id)
    self.executeQuery(query,value)
    self.commit()
    self.mycursor.close()

  def insertDataTransaksi(self,card_id,plate_number,status,price):
    self.mycursor = self.mydb.cursor(buffered=True)
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
    
    self.mycursor.close()
    return json_data

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
  
