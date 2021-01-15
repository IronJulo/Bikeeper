import serial
from PositionTragetProtocol import *
from AlertSendProtocol import *
from NormalSendProtocol import *

ser = serial.Serial('COM5')
ser.flushInput()

while True:

    dic1 = {}
    ser_bytes = ser.readline()
    decoded_bytes = str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
    #print(decoded_bytes)
    data = decoded_bytes.split(';')
    dic1['key'] = data[0]
    dic1['schema'] = data[1]
    dic1['sender'] = data[-1]
    s = dic1['schema']
    if s == "@":
        separated_values = PositionTarget(decoded_bytes)
    if s == "W":
        separated_values = AlertSend(decoded_bytes)
    if s == "*":
        separated_values = NormalSend(decoded_bytes)
    if s == "M":

    dic2 = separated_values.to_dico()
    dic = {**dic1, **dic2}
