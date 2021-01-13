import serial

ser = serial.Serial('COM3')
ser.flushInput()


while True:
    ser_bytes = ser.readline()
    try:
        decoded_bytes = str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
    except UnicodeDecodeError:
        pass
    print(decoded_bytes)

