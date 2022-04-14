import mysql.connector
from datetime import datetime,timedelta

class updateTable:
  def __init__(self,host,user,password,database):
    self.host = host
    self.user = user
    self.password = password
    self.database = database
  
  def connectDatabase(self):
    self.mydb = mysql.connector.connect(
    host=self.host,
    user=self.user,
    password=self.password,
    database=self.database
    )

  def executeQuery(self,query,val = None):
    self.mycursor = self.mydb.cursor()
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
    updateTable.executeQuery(self,query,value)
    updateTable.commit(self)
  
  def getPlateLatestTime(self):
    query = "Select hikvision_time from hikvision order by hikvision_time desc limit 1"
    updateTable.executeQuery(self,query)
    data = updateTable.fetchData(self)
    data = data[0][0] if len(data) > 0 else None
    return data
  

  def insertDataTransaksi(self,value):
    query = "insert into transaksi (transaksi_nama,transaksi_waktu) values(%s,%s)"
    value = ('dafi',value)
    updateTable.executeQuery(self,query,value)
    return updateTable.commit(self,True)

  def mergeLicenseTable(self,value_id,value_time):
    query = ("UPDATE hikvision \
              SET transaksi_id = %s \
              WHERE transaksi_id IS NULL \
              AND hikvision_time BETWEEN %s AND %s")
    value_time1 = value_time - timedelta(minutes = 3)
    value_time2 = value_time + timedelta(minutes = 1)
    value = (value_id,value_time1,value_time2)
    print(value)
    updateTable.executeQuery(self,query,value)
    updateTable.commit(self)
    

  def commit(self,id=None):
    self.mydb.commit()
    if id == None:
      print(self.mycursor.rowcount, "was inserted.")
    if id == True:
      print("1 record inserted, ID:", self.mycursor.lastrowid)
      return self.mycursor.lastrowid

if __name__ == "__main__":
 
  db = updateTable('localhost','root','root','tambangku')
  db.connectDatabase()


  print(db.getPlateLatestTime())
  # print(db.getPlateLatestTime())
  
