import flask
from flask import  request,jsonify,Response, render_template
from database2 import Databases_2
from time import sleep
from flask_cors import CORS,cross_origin
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import requests
from urllib.parse import urljoin
import base64
import json
from flask_sock import Sock


CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"

key1 = "MayoraInvesta@2022"
key2 = "TuhasAkhirISTTS@2022"

db = Databases_2()

app = flask.Flask(__name__)
sock = Sock(app)
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'


### Web Socket Control

### Creating Websocket instance to access CCTV img
@sock.route('/cctv_feed')
def echo(sock):
    while True:
        data = sock.receive()
        ### Confirm that request incoming is for img
        if "img" in data:
            ### Requesting image to local CCTV on every image requests
            try:
                imgBase64 = requests.get(f'http://admin:-arngnennscfrer2@192.168.2.64/Streaming/channels/1/picture', auth=HTTPDigestAuth("admin", "-arngnennscfrer2")).content
                base64_bytes = base64.b64encode(imgBase64).decode("utf-8")
                sock.send(base64_bytes)
            except Exception as e:
                print(e)
                sock.send({"message": "Not Authenticated"})
                
### Creating Websocket instance to access gate status
### This is necesary because long poll connection is more robust than requesting data on regular https
@sock.route('/gate')
def gate_ws(sock):
    while True:
        data = sock.receive()
        try:
            if "gate" in data:
                result = db.get_gate_status()
                
                if(len(result) > 0 ):
                    result = result[0]
                
                    result_object = json.dumps(result, indent = 4)
                    sock.send(result_object)
        except Exception as err:
            print(err)
            pass

### End of Websocket

### To set gate to open default id is 1, because we only have 1 gate for now
@app.route("/api/gate/open", methods=["get"])
def setGateOpen():
    print("Request Open")
    try:
        id = 1
        db.update_gate(1, id)
        return jsonify({'message': "data Accepted"})
    except:
        return jsonify({'Message': "Something Went Wrong"})

### To set gate to close
@app.route("/api/gate/close", methods=["get"])
def setGateClose():
    print("Request Close")
    try:
        id = 1
        db.update_gate(0, id)
        return jsonify({'message': "data Accepted"})
    except:
        return jsonify({'Message': "Something Went Wrong"})

### User Authentication
@app.route("/api/user/auth", methods=["post"])
def authenticateUser():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        username = request.json['username']
        password = request.json['password']
        result = db.get_user_auth(username, password)
        if result : return jsonify({"valid": True, "Message":"User Authenticated"})
        else : return jsonify({"valid": False, "Message":"User Not Authenticated"})

### Set Price
@app.route("/api/price/set", methods=["post"])
def setPrice():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        new_price = request.json['new_price']
        result = db.update_gate_price(new_price, 1)
        if result : return jsonify({"valid": True, "Message":"Price Updated"})
        else : return jsonify({"valid": False, "Message":"Price not Updated"})
    

app.run(host="0.0.0.0",port=6000)