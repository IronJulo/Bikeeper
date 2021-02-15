import requests
import serial
from PositionTrajetProtocol import *
from AlertSendProtocol import *
from NormalSendProtocol import *
import json

ser = serial.Serial('COM3')
ser.flushInput()

while True:
    ser_bytes = ser.readline()
    decoded_bytes = str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
    print(decoded_bytes)
    data = decoded_bytes.split(';')
    if data[0] == "[bk]":
        send_log(data)
    ser.flushInput()


def send_log(data):
    dic1 = {}
    dic1['key'] = data[0]
    dic1['schema'] = data[1]
    dic1['sender'] = "0" + data[-1][3:]
    s = dic1['schema']
    if s == "@":
        separated_values = PositionTrajet(data)
    if s == "W":
        separated_values = AlertSend(data)
    if s == "*":
        separated_values = NormalSend(data)
    if s == "M":
        pass

    dic2 = separated_values.to_dico()
    dic = {"header": dic1, "data": dic2}
    url = "http://127.0.0.1:5000/api/sms/add/"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=json.dumps(dic))
    print(response.text)
    print(dic)
