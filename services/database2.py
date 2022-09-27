import sys

import datetime
import MySQLdb as mdb
from authentication import AESCipher

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

### LIST OF USED QUERY ###
GET_USER_BY_ID = "SELECT * from card WHERE id LIKE %s"
GET_USER_BY_USERNAME = "SELECT * from card WHERE username LIKE %s"
GET_USER_BY_UID = "SELECT * from card WHERE uid LIKE %s"
GET_USER_PAGE = "SELECT * from card"
GET_GATE_STATUS = "SELECT * from gate where id = 1"
GET_TRANSACTION_LIST = "SELECT * from transaksi order by id desc"
GET_USER_AUTH = "SELECT * FROM user where username LIKE %s and password LIKE %s"

CREATE_USER = "INSERT INTO card (UID,keyA,saldo,username,email,phone) values(%s,%s,%s,%s,%s,%s)"
CREATE_TRANSACTION_LOG = "insert into transaksi (created_at,card_id,plate_number,status,price) values(%s,%s,%s,%s,%s)"

UPDATE_SALDO = "UPDATE card SET keyA= %s ,saldo = %s WHERE UID = %s"
UPDATE_GATE = "UPDATE gate SET gate = %s WHERE id = %s "
UPDATE_GATE_STATUS = "UPDATE gate SET gate_status = %s WHERE id = %s"
UPDATE_GATE_PRICE = "UPDATE gate SET price = %s WHERE id = %s"


### END OF LIST OF USED QUERY ###

class Databases_2:
    def __init__(self):
        self.DB_HOST = 'localhost'
        self.DB_USER = 'root'
        self.DB_PASSWORD = 'root'
        self.DB_NAME = 'tambangku'
    
    def get_user_auth(self, id, password):
        print("Trying to Authenticate")
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        results = []
        if con:
            print("Accessing Databases")
            cur = con.cursor()

            cur.execute(GET_USER_AUTH,(id,password))
            print("Execute Query")
            results = cur.fetchall()
            print("Fetching")
            cur.close()
            con.close()
        if len(results) > 0: return True
        else: return False

    def get_user_by_uid(self, uid):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        json_data = []
        if con:
            cur = con.cursor()
            cur.execute(GET_USER_BY_ID, (AESCipher(key2).encrypt(uid),))
            row_headers=[x[0] for x in cur.description]
            results = cur.fetchall()

            json_data = []
            for r in results:
                json_data.append(dict(zip(row_headers,r)))
            
            cur.close()
        if len(json_data) > 0 : return json_data[0]
        else : return []
    
    def get_user_page(self):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        json_data = []
        if con:
            cur = con.cursor()
            cur.execute(GET_USER_PAGE)
            row_headers=[x[0] for x in cur.description]
            results = cur.fetchall()

            
            for r in results:
                json_data.append(dict(zip(row_headers,r)))
            
            cur.close()
            con.close()
        return json_data
    
    def get_gate_status(self):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        json_data = []
        if con:
            cur = con.cursor()
            cur.execute(GET_GATE_STATUS)
            row_headers=[x[0] for x in cur.description]
            results = cur.fetchall()

            json_data = []
            for r in results:
                json_data.append(dict(zip(row_headers,r)))
            cur.close()
            con.close()
        if len(json_data) > 0 : return json_data
        else : return []
    
    def get_transaction_list(self):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        json_data = []
        if con:
            cur = con.cursor()
            cur.execute(GET_TRANSACTION_LIST)
            row_headers=[x[0] for x in cur.description]
            results = cur.fetchall()

            json_data = []
            for r in results:
                json_data.append(dict(zip(row_headers,r)))
            
            cur.close()
            con.close()
        return json_data
    
    def is_uid_exist(self, uid):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        if con:
            cur = con.cursor()

            cur.execute(GET_USER_BY_UID,(AESCipher(key2).encrypt(uid),))

            results = cur.fetchall()

            cur.close()
            con.close()
        if len(results) >0: return True
        else: return False
    
    def is_user_exist(self, username):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        results = []
        if con:
            cur = con.cursor()

            cur.execute(GET_USER_BY_USERNAME,(username,))

            results = cur.fetchall()

            cur.close()
            con.close()
        if len(results) > 0: return True
        else: return False

    
    def create_user(self,uid,key,saldo,username,email,phone):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        if con:
            # insert some data
            cur = con.cursor()
            value = (AESCipher(key2).encrypt(uid),AESCipher(str(saldo)).encrypt(key),AESCipher(key1).encrypt(str(saldo)),username,email,phone)
            cur.execute(CREATE_USER,value)

            affected_table = cur.rowcount

            con.commit()
            cur.close()
            print ("Number of rows updated: %d" % affected_table)
            return True
        return False
    
    def create_transaction_log(self,card_id,plate_number,status,price):
        con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        if con:
            created_at = datetime.datetime.now()
            # insert some data
            cur = con.cursor()
            value = (str(created_at)[0:19],card_id,plate_number,status,price)
            cur.execute(CREATE_TRANSACTION_LOG,value)

            affected_table = cur.rowcount

            con.commit()
            cur.close()
            print ("Number of rows updated: %d" % affected_table)
            return True
        return False

    
    def update_saldo(self,key_access,uid,newSaldo):
        try:
            con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
            # insert some data
            cur = con.cursor()
            value = (AESCipher(str(key_access)).encrypt(newSaldo),newSaldo,uid)
            cur.execute(UPDATE_SALDO,value)

            affected_table = cur.rowcount

            con.commit()
            cur.close()
            print ("Number of rows updated: %d" % affected_table)
            return True
        except mdb.Error as e:
            print ('Time to Rollback..')
            con.rollback()
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            return False
        except Exception as err:
            print(err)
            return False
    
    def update_gate(self, gate, id):
        try:
            con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
            # insert some data
            cur = con.cursor()
            value = (gate,id)
            cur.execute(UPDATE_GATE,value)

            affected_table = cur.rowcount

            con.commit()
            cur.close()
            print ("Number of rows updated: %d" % affected_table)
            return True
        except mdb.Error as e:
            print ('Time to Rollback..')
            con.rollback()
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            return False
        except Exception as err:
            print(err)
            return False

    def update_gate_status(self, gate, id):
        try:
            con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
            # insert some data
            cur = con.cursor()
            value = (gate,id)
            cur.execute(UPDATE_GATE_STATUS,value)

            affected_table = cur.rowcount

            con.commit()
            cur.close()
            return True
        except mdb.Error as e:
            print ('Time to Rollback..')
            con.rollback()
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            return False
        except Exception as err:
            print(err)
            return False

    def update_gate_price(self, price, id):
        try:
            con = mdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
            # insert some data
            cur = con.cursor()
            value = (price,id)
            cur.execute(UPDATE_GATE_PRICE,value)

            affected_table = cur.rowcount

            con.commit()
            cur.close()
            print ("Number of rows updated: %d" % affected_table)
            return True
        except mdb.Error as e:
            print ('Time to Rollback..')
            con.rollback()
            print ("Error %d: %s" % (e.args[0], e.args[1]))
            return False
        except Exception as err:
            print(err)
            return False
    
    
            
if __name__ == "__main__":
    test = Databases_2()
    ## Testing 500 Queries
    # for _ in range(500):
    #     print(test.update_gate(1,1))
    #     print(test.update_gate_status(1,1))
    #     print(test.update_gate_price(7000,1))
    #     print(test.is_user_exist("dafi"))
    #     print(test.get_user_page())
    print(test.update_gate(1,1))
    print(test.update_gate_status(1,1))
    print(test.update_gate_price(7000,1))
    print(test.create_transaction_log(1, "", 1,3000))
    print(test.is_user_exist("dafi"))
    print(test.get_user_page())