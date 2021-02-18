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
                                        ║ [ ]A2     ╚═══╝           INT1/3[ ]~║
                                        ║ [ ]A3                     INT0/2[ ] ║══════> Interrupt pin for the "do" pin of the vibration sensor
                                        ║ [ ]A4/SDA  RST SCK MISO     TX>1[ ] ║
                                        ║ [ ]A5/SCL  [ ] [ ] [ ]      RX<0[ ] ║
                                        ║            [ ] [ ] [ ]              ║
                                        ║            GND MOSI 5V ╔════════════╝
                                        ╚═══UNO_R3═══════════════╝ 
*/

#include <Arduino.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h> // for Sim800L & Tinygps++
#include <string.h>

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"
/*#include "SmsFormatter.hpp"*/
#include "Utils.hpp"

/*#include "Headers/messageHeader.h"
#include "Headers/messageAlert.h"
#include "Headers/messageTrajet.h"
#include "Headers/messageHeartbeat.h"
#include "Headers/messageReceived.h"*/
#include "Headers/location.h"

/* Sim800L */
#define SERVER_PHONE_NUMBER "+33769342048" // BiKServer number (main server) called to get user number

char userPhoneNumber[13] = "";

#define GSM_BAUDRATE 9600
#define GSM_RX 7
#define GSM_TX 8

SoftwareSerial softwareSim800l(GSM_RX, GSM_TX);

char sms_storage[100];
StringBuffer sms_buffer(sms_storage, sizeof(sms_storage));

char message_storage[70];
StringBuffer message_buffer(message_storage, sizeof(message_storage));
//SmsFormatter smsFormatter(&message_buffer);                              //Not used all the time but to simplify coordinate

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
#define DEVICE_BATTERY_PIN 0 // Declare the device battery (analog)
#define BIKE_BATTERY_PIN 1	 // Declare the device battery (analog)

int deviceBatteryLevel = 0;
int bikeBatteryLevel = 0;

bool isBatteryCharging = false;
/* Battery sensor */

/* GPS */
#define GPS_RX 4 // Declare the SIM800L onto the pin 7.
#define GPS_TX 3

#define GPS_BAUDRATE 9600
TinyGPSPlus gps;

location_t location; // Declare the Location type
SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
bool bikeMoved = false;
#define GPS_TRESHOLD_LAT 0.000011
#define GPS_TRESHOLD_LON 0.000020
/* GPS */
/* Angle Detection */

bool bikeFallen = false;
#define FALL_CALL_TIMEOUT 60000 // 1 minute 
#define FALL_ANGLE /* TODO */ // 1 minute 
unsigned long fallTime = 0;
/* Angle Detection */
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
}

void loop()
{
	actualizeLocation();
	actualizeDeviceBattery();
	actualizeBikeBattery();
	actualizeIsBatteryCharging();

	if (parked)
	{
		//interrupts();
		if (vibartion)
		{
			vibartion = false;
			Serial.println("vibred moto*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*");
			/* TODO CODE send sms vibration */
		}

		if (bikeMoved)
		{
			bikeMoved = false;
			Serial.println("mouved moto*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*");

			/* TODO CODE send sms moved */
		}
	}
	/*else 
	{
		noInterrupts();
	}*/

	if (bikeFallen && fallTime - millis() >= FALL_CALL_TIMEOUT)							// If the bike has fallen && user didn't respond in 60000 miliseconds 
	{
		/* TODO CODE send sms bike fallen */
	}




	Serial.println(F("latitude"));
	printFloat(location.latitude, 1, 11, 6);
	Serial.println();
	Serial.println(F("longitude"));
	printFloat(location.longitude, 1, 12, 6);
	Serial.println();
	Serial.println();

	Serial.println("waiting command");
	Serial.println();

	readIncommingSms();
	smartDelay(1000);
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
	sim800L.deleteALLRead();
	sim800L.carriageReturn();
	sim800L.setModeTexte();
	sim800L.carriageReturn();
	sim800L.carriageReturn();
	sim800L.carriageReturn();
	sim800L.carriageReturn();

	if (sim800L.smartRead("+CMTI", 5, 1000))
	{
		Serial.println(sms_buffer.getStorage());
		sim800L.setModeTexte();
		sim800L.carriageReturn();
		sim800L.smartRead("+CMTI", 5, 1000);
		Serial.println(sms_buffer.getStorage());
		treatSMS();
	}
}

void actualizeLocation()
{
	noInterrupts();
	gpsSerial.listen();
	printFloat(location.latitude - gps.location.lat(), 1, 12, 6);
	Serial.println();
	printFloat(location.longitude - gps.location.lng(), 1, 12, 6);
	Serial.println();

	if (location.latitude - gps.location.lat() >= GPS_TRESHOLD_LAT ||
		location.latitude - gps.location.lat() <= -GPS_TRESHOLD_LAT ||
		location.longitude - gps.location.lng() >= GPS_TRESHOLD_LON ||
		location.longitude - gps.location.lng() <= -GPS_TRESHOLD_LON)
	{
		bikeMoved = true;
	}
	location.latitude = gps.location.lat();
	location.longitude = gps.location.lng();
	sim800L.listen();
	interrupts();
}

void actualizeDeviceBattery()
{
	//TODO implement this ok!
	deviceBatteryLevel = 50;
}

void actualizeBikeBattery()
{
	//TODO implement this ok!
	bikeBatteryLevel = 42;
}

void actualizeIsBatteryCharging()
{
	isBatteryCharging = false;
}

void vibartionDetected()
{
	vibartion = true;
}