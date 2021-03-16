import serial

ser = serial.Serial('COM3')
ser.flushInput()

ser.write(b'+33769342048;0631704631')