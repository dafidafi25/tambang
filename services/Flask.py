import flask
from flask import  request,jsonify,Response, render_template
from database import databases
from time import sleep
from flask_cors import CORS,cross_origin
from smartcard.util import *
from requests.sessions import TooManyRedirects
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib.parse import urljoin
import base64
import json
import cv2
import argparse
import threading
from flask_sock import Sock


CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

db = databases('localhost','root','root','tambangku')
db.connectDatabase()

app = flask.Flask(__name__)
sock = Sock(app)
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@sock.route('/cctv_feed')
def echo(sock):
    while True:
        data = sock.receive()
        if "img" in data:
            try:
                imgBase64 = requests.get(f'http://admin:-arngnennscfrer2@192.168.2.64/Streaming/channels/1/picture', auth=HTTPDigestAuth("admin", "-arngnennscfrer2")).content
                base64_bytes = base64.b64encode(imgBase64).decode("utf-8")
                sock.send(base64_bytes)
            except Exception as e:
                print(e)
                sock.send({"message": "Not Authenticated"})
                

@sock.route('/gate')
def gate_ws(sock):
    while True:
        data = sock.receive()
        try:
            if "gate" in data:
                result = db.getGateStatus()
                if(len(result) > 0 ):
                    result = result[0]
                
                    result_object = json.dumps(result, indent = 4)
                    sock.send(result_object)
            elif "set_gate" in data:
                print("Gate Set")
                data = data['set_gate']
                if data is 1 : db.setGate(1,1)
                if data is 0 : db.setGate(0,1)
        except Exception as err:
            print(err)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/api/register",methods = ['POST']) #(,uid,key,saldo,username,email,phone)
def register():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        username = request.json['username']
        email = request.json['email']
        phone = request.json['phone']
        saldo = request.json['saldo']
        uid = request.json['uid']
        key = request.json['key']
        result = db.register(uid,key,int(saldo),username,email,phone)

        if   result == False:
            return jsonify({"Message":"Username / UID sudah terdaftar"}),302
        else:
            return jsonify({"Message":"Data Added"}),202            

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
        if len(result) > 0 : return jsonify(result[0])
        else : return jsonify({"Message":"Data Not Found"}),302

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

@app.route("/api/gate", methods=["GET"])
def getGateStatus():
    result = db.getGateStatus()
    print(result)
    if len(result) > 0 : return jsonify(result[0])
    else : return jsonify({"Message":"Data Not Found"}),302

@app.route("/api/gate/open", methods=["get"])
def setGateOpen():
    print("Request Open")
    try:
        id = 1
        db.setGate(1, id)
        return jsonify({'message': "data Accepted"})
    except:
        return jsonify({'Message': "Something Went Wrong"})


@app.route("/api/gate/close", methods=["get"])
def setGateClose():
    print("Request Close")
    try:
        id = 1
        db.setGate(0, id)
        return jsonify({'message': "data Accepted"})
    except:
        return jsonify({'Message': "Something Went Wrong"})


@app.route("/api/gate/set/gate_status", methods=["POST"])
def setGateStatus():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        gate_status = request.json['gate_status']
        id = 1
        result = db.setGateStatus(gate_status, id)
        return jsonify(result)

@app.route("/api/gate/set/price", methods=["POST"])
def setPrice():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        price = request.json['price']
        id = 1
        result = db.setPrice(price, id)
        if len(result) > 0 : return jsonify(result[0])
        else : return jsonify({"Message":"Data Not Found"}),302




app.run(host="0.0.0.0",port=6000)