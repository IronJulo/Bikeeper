import serial

ser = serial.Serial('COM3')
ser.flushInput()

ser.write(b'Test envoie message;0769342048')