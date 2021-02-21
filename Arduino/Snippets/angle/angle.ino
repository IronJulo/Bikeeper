// (c) Michael Schoeffler 2017, http://www.mschoeffler.de

#include <Wire.h> // This library allows you to communicate with I2C devices.

const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.

#define GYRO_MIN_MAX 16000

//#define GYRO_X_MIN_MAX 16300

//int16_t accelerometer_x, accelerometer_y, accelerometer_z; // variables for accelerometer raw data
double gyro_y, gyro_x; // variables for gyro raw data
short zeroGyro_y, zeroGyro_x = 0; // variables for gyro raw data
//int16_t temperature; // variables for temperature data

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR); // Begins a transmission to the I2C slave (GY-521 board)
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
}
void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
  Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
  Wire.requestFrom(MPU_ADDR, 2*2, true); // request a total of 7*2=14 registers
  /*// "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
  accelerometer_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  temperature = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)*/
  gyro_y = Wire.read()<<8 | Wire.read();
  gyro_x = Wire.read()<<8 | Wire.read();
  //gyro_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
    if (zeroGyro_y == 0 || zeroGyro_x == 0)
  {
      zeroGyro_y = gyro_y; // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
      zeroGyro_x = gyro_x;
  }
  gyro_x  = (gyro_x - zeroGyro_x) / GYRO_MIN_MAX_X * 90; // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  gyro_y =  (gyro_y - zeroGyro_y) / GYRO_MIN_MAX_Y * 90; // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)

  // print out data
  /*Serial.print("aX = "); Serial.print(accelerometer_x);
  Serial.print(" | aY = "); Serial.print(accelerometer_y);
  Serial.print(" | aZ = "); Serial.print(accelerometer_z);
  // the following equation was taken from the documentation [MPU-6000/MPU-6050 Register Map and Description, p.30]
  Serial.print(" | tmp = "); Serial.print(temperature/340.00+36.53);*/
  Serial.print(" | AngX = "); Serial.print(gyro_x);
  Serial.print(" | AngY = "); Serial.print(gyro_y);
  Serial.print(" | zeroGyro_x = "); Serial.print(zeroGyro_x);
  Serial.print(" | zeroGyro_y = "); Serial.print(zeroGyro_y);
  //Serial.print(" | AngZ = "); Serial.print(gyro_z);
  Serial.println();
  
  // delay
  delay(1000);
}
