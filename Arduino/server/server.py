import serial
from PositionTrajetProtocol import *
from AlertSendProtocol import *
from NormalSendProtocol import *

ser = serial.Serial('COM3')
ser.flushInput()

while True:

    dic1 = {}
    ser_bytes = ser.readline()
    decoded_bytes = str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
    print(decoded_bytes)
    data = decoded_bytes.split(';')
    if data[0] == "[bk]":
        dic1['key'] = data[0]
        dic1['schema'] = data[1]
        dic1['sender'] = data[-1]
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
        dic = {**dic1, **dic2}
        
        print(dic)
