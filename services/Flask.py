import flask
from flask import  request,jsonify,Response
from services.database import databases
from time import sleep
from smartCard2 import smartCard
from flask_cors import CORS,cross_origin
from smartcard.util import *


CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

db = databases('localhost','root','root','tambangku')
db.connectDatabase()

BASIC_AUTH_KEY = [0xff,0xff,0xff,0xff,0xff,0xff]
BASIC_ACCESS_BITS = [0xff,0x07,0x80]

SECTOR = [4*0,4*1,4*2,4*3,4*4,4*5,4*6,4*7,4*8,4*9,4*10,4*11,4*12,4*13,4*14,4*15]



app = flask.Flask(__name__)
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/register",methods = ['POST']) #(,uid,key,saldo,username,email,phone)
def register():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        smartCardControl = smartCard()
        smartCardControl.connect()
        username = request.json['username']
        email = request.json['email']
        phone = request.json['phone']
        saldo = request.json['saldo']
        if smartCardControl.isNewCard():
            uid = smartCardControl.readCard()
            block,key =  smartCardControl.getValueBlockFormat(int(saldo),11*4+1)
            key = toHexString(key)

            # smartCardControl.setWalletSector(int(saldo),10)

            result = db.register(uid,key,int(saldo),username,email,phone)
            print(result)
            if   result == False:
                return jsonify({"Message":"Username / UID sudah terdaftar"}),302
            else:
                return jsonify({"Message":"Data Added"}),202
        else:
            
            return jsonify({"Message":"RFID Tag Tidak Terdeteksi"}),201

@app.route("/api/card/page", methods=["GET"])
def cardByPage():
    data = db.getUserPage(1,1) 
    return jsonify({
        "data" : data,
        "Message" : "Post Request Success"
    }),202

@app.route("/api/validate/uid", methods=["POST"])
def validateByUid():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        uidChiper = request.json['uid']
        result = db.isUidExist(uidChiper)
        return jsonify(result)

@app.route("/api/get/user/uid", methods=["POST"])
def getUserByUid():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        uidChiper = request.json['uid']
        result = db.getUserByUid(uidChiper)
        return jsonify(result)

@app.route("/api/price/get", methods=["get"])
def getDevicePrice():
    result = db.getDevicePrice()
    return jsonify(result)

@app.route("/api/transaction", methods=["POST"])
def insertTransaction():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        id = request.json['id']
        plate_number = request.json['plate_number']
        price = request.json['price']
        result = db.insertDataTransaksi(id,plate_number,1,price)
        return jsonify(result)

@app.route("/api/saldo", methods=["POST"])
def updateSaldo():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        saldo = request.json['saldo']
        key = request.json['key']
        uid = request.json['uid']
        result = db.updateSaldo(key,uid,saldo)
        return jsonify(result)

@app.route("/api/transaksi/list", methods=["GET"])
def getTransaksiList():
    result = db.getListTransaksi()
    return jsonify(result)



app.run(host="0.0.0.0",port=6000)