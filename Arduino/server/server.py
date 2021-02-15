import requests
import serial
from PositionTrajetProtocol import *
from AlertSendProtocol import *
from NormalSendProtocol import *
import json

ser = serial.Serial('COM3')
ser.flushInput()

def send_log(dic1, separated_values):
    dic2 = separated_values
    dic = {"header": dic1, "data": dic2}
    url = "http://127.0.0.1:5000/api/sms/add/"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=json.dumps(dic))
    print(response.text)
    print(dic)

def init(dic1):
    url = "http://127.0.0.1:5000/api/bikeeper/get_user_num/0664277796"
    response = requests.request("GET", url)
    if response.json["type_message"] == "response_num":
        ser.write((response.json()["numero"] + ';0769342048').encode())

while True:
    ser_bytes = ser.readline()
    decoded_bytes = str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
    print(decoded_bytes)
    data = decoded_bytes.split(';')
    if data[0] == "[bk]":
        dic1 = {}
        dic1['key'] = data[0]
        dic1['schema'] = data[1]
        dic1['sender'] = "0" + data[-1][3:]
        s = dic1['schema']
        if s == "@":
            send_log(dic1,PositionTrajet(data).to_dico())
        elif s == "W":
            send_log(dic1,AlertSend(data).to_dico())
        elif s == "*":
            send_log(dic1,NormalSend(data).to_dico())
        elif s == "+":
            send_log(dic1, {"type": data[2]})
        elif s == "I":
            init(dic1)
        elif s == "M":
            pass

    ser.flushInput()
