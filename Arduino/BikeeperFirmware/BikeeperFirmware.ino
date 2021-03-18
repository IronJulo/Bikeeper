/*
for the arduino uno
                                             ╔═══╗                   ╔═════╗
                                        ╔════╣PWR╠═══════════════════╣ USB ╠══╗
                                        ║    ╚═══╝                   ╚═════╝  ║
                                        ║         GND/RST2  [ ][ ]            ║
                                        ║       MOSI2/SCK2  [ ][ ]  A5/SCL[ ] ║ 
                                        ║          5V/MISO2 [ ][ ]  A4/SDA[ ] ║
                                        ║                             AREF[ ] ║
                                        ║                              GND[ ] ║
                                        ║ [ ]N/C                    SCK/13[ ] ║
                                        ║ [ ]IOREF                 MISO/12[ ] ║
                                        ║ [ ]RESET                 MOSI/11[ ]~║
                                        ║ [ ]3V3    ╔═══╗               10[ ]~║
  +5V (2A) external power supply <══════║ [ ]5v    ═╣ A ╠═               9[ ]~║
    Ground external power supply <══════║ [ ]GND   ═╣ R ╠═               8[ ] ║══════> SIM800L rx 
                                        ║ [ ]GND   ═╣ D ╠═                    ║
                                        ║ [ ]Vin   ═╣ U ╠═               7[ ] ║══════> SIM800L tx
                                        ║          ═╣ I ╠═               6[ ]~║
                                        ║ [ ]A0    ═╣ N ╠═               5[ ]~║
                                        ║ [ ]A1    ═╣ O ╠═               4[ ] ║══════> GPS tx
                    Bike battery <══════║ [ ]A2     ╚═══╝           INT1/3[ ]~║
                  Device battery <══════║ [ ]A3                     INT0/2[ ] ║══════> Interrupt pin for the "do" pin of the vibration sensor
                   Gyroscope SDA <══════║ [ ]A4/SDA  RST SCK MISO     TX>1[ ] ║
                   Gyroscope SCL <══════║ [ ]A5/SCL  [ ] [ ] [ ]      RX<0[ ] ║
                                        ║            [ ] [ ] [ ]              ║
                                        ║            GND MOSI 5V ╔════════════╝
                                        ╚═══UNO_R3═══════════════╝ 
*/

#include <Arduino.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h> // for Sim800L & Tinygps++
#include <string.h>
#include "Wire.h"

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"
#include "SmsFormatter.hpp"
#include "Utils.hpp"

/*#include "Headers/messageHeader.h"
#include "Headers/messageAlert.h"
#include "Headers/messageTrajet.h"
#include "Headers/messageHeartbeat.h"
#include "Headers/messageReceived.h"*/
#include "Headers/location.h"

/* Sim800L */
// and +33664277796
#define SERVER_PHONE_NUMBER "+33664277796" // BiKServer number (main server) called to get user number

char userPhoneNumber[13] = "";

#define GSM_BAUDRATE 9600
#define GSM_RX 7
#define GSM_TX 8

SoftwareSerial softwareSim800l(GSM_RX, GSM_TX);

char sms_storage[150];
StringBuffer sms_buffer(sms_storage, sizeof(sms_storage));

char message_storage[80];
StringBuffer message_buffer(message_storage, sizeof(message_storage));
SmsFormatter smsFormatter(&message_buffer); //Not used all the time but to simplify sms generation

I_Sim800L sim800L(&softwareSim800l, &sms_buffer);
/* Sim800L */

/* States */
bool parked = false;
bool journey = false;
/* States */

/* Vibration sensor */
bool vibartion = false; // False most of the time but true if the module detected a vibration (trough interrupt)
#define VIBRATION 'V'
/* Vibration sensor */

/* Battery sensor */
#define DEVICE_BATTERY_PIN A3 // Declare the device battery (analog)
#define BIKE_BATTERY_PIN A2	 // Declare the device battery (analog)

#define deviceMaxBatteryVoltage 1024 //verify later
#define bikeMaxBatteryVoltage 1024 // verify later

double deviceBatteryLevel = 0;
double bikeBatteryLevel = 0;

bool isBatteryCharging = false;
/* Battery sensor */

/* GPS */
#define GPS_RX 4 // Declare the SIM800L onto the pin 7.
#define GPS_TX 3

#define GPS_BAUDRATE 9600
TinyGPSPlus gps;

location_t location; // Declare the Location type
int bikeSpeed = 0;
SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
bool bikeMoved = false;
#define GPS_TRESHOLD_LAT 0.000100 //0.000011
#define GPS_TRESHOLD_LON 0.000100 //0.000020
/* GPS */

/* Angle Detection */
#define GYRO_MIN_MAX_X 16000
#define GYRO_MIN_MAX_Y 17600
#define FALL_CALL_TIMEOUT 60000 // 1 minute
#define ANGLE_TRESHOLD 800 // Max angle before threating it as a fall 

const int MPU_ADDR = 0x68;
bool bikeFallen = false;
double gyro_y, gyro_x;
short zeroGyro_y, zeroGyro_x = 0;
unsigned long fallTime = 0;
/* Angle Detection */



/* heartbeat */
#define HEARTBEAT_TIMEOUT 20000 //time between each heart beat sms
unsigned long lastHeartbeatTime = millis();

/* heartbeat */
void setup()
{
	Serial.begin(9600);
	gpsSerial.begin(GPS_BAUDRATE);
	sim800L.begin(GSM_BAUDRATE);

	sim800L.init(userPhoneNumber, SERVER_PHONE_NUMBER);

	message_buffer.clear();
	strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringSyncOk])));

	sim800L.send(userPhoneNumber, message_buffer.getStorage());

	attachInterrupt(0, vibartionDetected, RISING); // Interrupt for the vibration detector (RISING because the detector emmit ~3.5V for 10 ms).

	Serial.println(message_buffer.getStorage());
	message_buffer.clear();
	sim800L.smartRead("+CMGS", 5, 30000);
	sim800L.deleteALL();
	sim800L.setModeTexte();
	sim800L.smartRead("OK", 2, 500);

	Wire.begin();
	Wire.beginTransmission(MPU_ADDR);
	Wire.write(0x6B);
	Wire.write(0);
	Wire.endTransmission(true);

	interrupts();
}

void loop()
{
	actualizeLocation();
	actualizeBatterys();
	actualizeIsBatteryCharging();
	actualizeAngle();
	if (parked)
	{
		//interrupts();
		if (vibartion) /* TODO timeout */
		{
			vibartion = false;
			message_buffer.clear();

			strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringVibrationDetected])));
			sim800L.send(userPhoneNumber, message_buffer.getStorage());
			sim800L.smartRead("+CMGS", 5, 1000);
			delay(1500);

			message_buffer.clear();

			smsFormatter.makeAlertSms('W', 'V', &location, isBatteryCharging, deviceBatteryLevel, bikeBatteryLevel);
			sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
			sim800L.smartRead("+CMGS", 5, 1000);

			delay(100);

			message_buffer.clear();
		}

		if (bikeMoved)
		{
			bikeMoved = false;

			message_buffer.clear();

			strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringMovementDetected])));
			sim800L.send(userPhoneNumber, message_buffer.getStorage());
			sim800L.smartRead("+CMGS", 5, 1000);
			delay(1000);

			message_buffer.clear();
			
			smsFormatter.makeAlertSms('W', 'G', &location, isBatteryCharging, deviceBatteryLevel, bikeBatteryLevel);
			sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
			sim800L.smartRead("+CMGS", 5, 1000);
			delay(100);



			message_buffer.clear();
		}
	}
	if (bikeFallen && fallTime == 0)
	{
		gyro_x = 0;
		gyro_y = 0;
		fallTime = millis();
		message_buffer.clear();

		strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringFallDetected])));
		sim800L.send(userPhoneNumber, smsFormatter.getStorage());
		delay(100);
		Serial.println(smsFormatter.getStorage());

		message_buffer.clear();
	}

	if (bikeFallen && millis() - fallTime >= FALL_CALL_TIMEOUT) // If the bike has fallen && user didn't respond in FALL_CALL_TIMEOUT miliseconds
	{
		gyro_x = 0;
		gyro_y = 0;
		bikeFallen = false;
		fallTime = 0;
		smsFormatter.makeAlertSms('W', 'F', &location, isBatteryCharging, deviceBatteryLevel, bikeBatteryLevel);
		sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
		delay(500);

		/* TODO alert the user that we called is contacts */
	}

	if (!bikeFallen && millis() - lastHeartbeatTime >= HEARTBEAT_TIMEOUT ) // if it has beed heartbeat_timeout time since last heart beat sms send
	{
		lastHeartbeatTime = millis();
		if(journey)
		{
			int gyro_int_y = gyro_y;
			Serial.println("gyro_int_y before print --------------");
			Serial.println(gyro_int_y);
			Serial.println("--------------------");
			smsFormatter.makeJourneySms('@', &location, isBatteryCharging, deviceBatteryLevel, bikeBatteryLevel, bikeSpeed, gyro_int_y);
			Serial.println("smsFormatter.getStorage()");
			Serial.println(smsFormatter.getStorage());
			sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
			sim800L.smartRead("+CMGS", 5, 500);
			delay(500);
		}else
		{
			smsFormatter.makeHeartbeatSms('*', &location, isBatteryCharging, deviceBatteryLevel, bikeBatteryLevel);
			Serial.println("smsFormatter.getStorage()");
			Serial.println(smsFormatter.getStorage());
			sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
			sim800L.smartRead("+CMGS", 5, 500);
			delay(500);
		}
	}
	Serial.println("gyro ---------------");
	Serial.println("gyro_x");
	Serial.println(gyro_x);
	Serial.println("gyro_y");
	Serial.println(gyro_y);

	Serial.println("pos ----------------");
	Serial.println("latitude");
	printFloat(location.latitude , 1, 12, 6);
	Serial.println();
	Serial.println("longitude");
	printFloat(location.longitude , 1, 12, 6);
	Serial.println();

	Serial.println("speed --------------");
	Serial.println(bikeSpeed);
	Serial.println("--------------------");

	smartDelay(2000);
	readIncommingSms();

	/*smsFormatter.makeJourneySms('@', &location, isBatteryCharging, deviceBatteryLevel, bikeBatteryLevel, bikeSpeed, 40);
	Serial.println("smsFormatter.getStorage()");
	Serial.println(smsFormatter.getStorage());*/
	//delay(2000);
}

static void smartDelay(unsigned long ms)
{
	gpsSerial.listen();
	unsigned long start = millis();
	do
	{
		while (gpsSerial.available())
			gps.encode(gpsSerial.read());
	} while (millis() - start < ms);
	sim800L.listen();
}

static void printFloat(float val, bool valid, int len, int prec)
{
	if (!valid)
	{
		while (len-- > 1)
			Serial.print('*');
		Serial.print(' ');
	}
	else
	{
		Serial.print(val, prec);
		int vi = abs((int)val);
		int flen = prec + (val < 0.0 ? 2 : 1); // . and -
		flen += vi >= 1000 ? 4 : vi >= 100 ? 3
							 : vi >= 10	   ? 2
										   : 1;
		for (int i = flen; i < len; ++i)
			Serial.print(' ');
	}
	delay(0);
}

void readIncommingSms()
{
	if (sms_buffer.indexOf("+CMTI", 5) != -1)
	{
		Serial.println("sms_buffer.getStorage()");
		Serial.println(sms_buffer.getStorage());
		treatSMS();
		return;
	}
	sim800L.carriageReturn();

	sim800L.deleteALLRead();
	sim800L.carriageReturn();
	sim800L.setModeTexte();
	sim800L.carriageReturn();

	if (sim800L.smartRead("+CMGR", 5, 1000))
	{
		//if (sms_buffer.indexOf("+CMTI", 5) != -1)
		//{
			Serial.println("sim800L.smartRead(, 5, 1000)");
			Serial.println(sms_buffer.getStorage());
			sim800L.setModeTexte();
			sim800L.carriageReturn();
			sim800L.smartRead("+CMTI", 5, 1000);
			Serial.println(sms_buffer.getStorage());
			treatSMS();
		//}
	}
}

void actualizeLocation()
{
	//noInterrupts();
	gpsSerial.listen();

	if (location.latitude - gps.location.lat() >= GPS_TRESHOLD_LAT ||
		location.latitude - gps.location.lat() <= -GPS_TRESHOLD_LAT ||
		location.longitude - gps.location.lng() >= GPS_TRESHOLD_LON ||
		location.longitude - gps.location.lng() <= -GPS_TRESHOLD_LON) // Calcul delta pos
	{
		bikeMoved = true;
	}
	location.latitude = gps.location.lat();
	location.longitude = gps.location.lng();
	bikeSpeed = gps.speed.kmph();
	sim800L.listen();
	//interrupts();
}

void actualizeBatterys()
{
	deviceBatteryLevel = 42;//(analogRead(A3)/deviceMaxBatteryVoltage*100);
	bikeBatteryLevel = 69;//(analogRead(A3)/bikeMaxBatteryVoltage*100);
}

void actualizeIsBatteryCharging()
{
	isBatteryCharging = false;
}

void actualizeAngle()
{
	Wire.beginTransmission(MPU_ADDR);
	Wire.write(0x3B);

	Wire.endTransmission(false);
	Wire.requestFrom(MPU_ADDR, 2 * 2, true);

	gyro_y = Wire.read() << 8 | Wire.read();
	gyro_x = Wire.read() << 8 | Wire.read();

	if (zeroGyro_y == 0 || zeroGyro_x == 0)
	{
		zeroGyro_y = gyro_y;
		zeroGyro_x = gyro_x;
	}
	gyro_x = (gyro_x - zeroGyro_x) / GYRO_MIN_MAX_X * 90;
	gyro_y = (gyro_y - zeroGyro_y) / GYRO_MIN_MAX_Y * 90;


	if (fallTime == 0 && 
		//gyro_x >= ANGLE_TRESHOLD ||
		//gyro_x <= -ANGLE_TRESHOLD ||
		gyro_y >= ANGLE_TRESHOLD ||
		gyro_y <= -ANGLE_TRESHOLD)
	{
		bikeFallen = true;
	}
	Wire.endTransmission(true);
}

void vibartionDetected()
{
	vibartion = true;
}
