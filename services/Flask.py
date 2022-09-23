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
            full_url = urljoin('http://'+'192.168.2.64' + ':'+ '80', '/ISAPI/System/status')
            session = requests.session()
            session.auth = HTTPBasicAuth('admin', '-arngnennscfrer2')
            try:
                response = session.get(full_url)
                if response.status_code == 401:
                    session.auth = HTTPDigestAuth('admin', '-arngnennscfrer2')
                    response = session.get(full_url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(e)
                sock.send({"message": "Not Authenticated"})
            else:
                response = session.request( method='get', url= 'http://'+'192.168.2.64' + ':'+ '80' + "/ISAPI/Streaming/channels/1/picture?videoResolutionWidth=640&videoResolutionHeight=480", timeout=3, stream=True).content
                base64_bytes = base64.b64encode(response).decode("utf-8")
                sock.send(base64_bytes)

@sock.route('/gate')
def gate_ws(sock):
    while True:
        data = sock.receive()
        data = json.loads(data)
        if "gate" in data:
            result = db.getGateStatus()
            sock.send(result[0])
        elif "set_gate" in data:
            data = data['set_gate']
            print(data)
            if data is 1 : db.setGate(1,1)
            if data is 0 : db.setGate(0,1)

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

@app.route("/api/gate", methods=["GET"])
def getGateStatus():
    result = db.getGateStatus()
    print(result)
    if len(result) > 0 : return jsonify(result[0])
    else : return jsonify({"Message":"Data Not Found"}),302

@app.route("/api/gate/set/gate", methods=["POST"])
def setGate():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        gate = request.json['gate']
        id = 1
        result = db.setGate(gate, id)
        return jsonify(result)

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