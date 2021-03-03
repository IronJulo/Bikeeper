import requests
import serial
from PositionTrajetProtocol import *
from AlertSendProtocol import *
from NormalSendProtocol import *
import json
from time import sleep
from unidecode import unidecode

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
    url = f"http://127.0.0.1:5000/api/bikeeper/get_user_num/{dic1['sender']}"
    response = requests.request("GET", url)
    if response.json["type_message"] == "response_num":
        ser.write((response.json()["numero"] + f';{dic1["sender"]}').encode())


def alert_fall(dic1, lat, lon):
    url = f"http://127.0.0.1:5000/api/bikeeper/contacts/{dic1['sender']}"
    response = requests.request("GET", url).json()
    for contact in response["contacts"]:
        print("sending")
        msg = f'{unidecode(contact["lastname_contact"])} {unidecode(contact["firstname_contact"])}, {unidecode(response["bikeeper_owner"])} est tombe de sa moto a {(str(float(lon)*1000))[0:10]}, {(str(float(lat)*1000))[0:10]};{contact["num_contact"]}'
        print(msg)
        print(len(msg))
        ser.write(msg.encode())
        print("wait")
        sleep(2)
    print(response)

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
            send_log(dic1, PositionTrajet(data).to_dico())
        elif s == "W":
            if data[2] == "F":
                alert_fall(dic1, data[3], data[4])
            send_log(dic1, AlertSend(data).to_dico())
        elif s == "*":
            send_log(dic1, NormalSend(data).to_dico())
        elif s == "+":
            send_log(dic1, {"type": data[2]})
        elif s == "I":
            init(dic1)

    ser.flushInput()
