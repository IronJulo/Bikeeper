/*
for the arduino uno
                                             ╔═══╗                   ╔═════╗
                                        ╔════║PWR║═══════════════════║ USB ║══╗
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
  +5V (2A) external power supply <══════║ [ ]5v    ═║ A ║═               9[ ]~║
    Ground external power supply <══════║ [ ]GND   ═║ R ║═               8[ ] ║══════> SIM800L rx 
                                        ║ [ ]GND   ═║ D ║═                    ║
                                        ║ [ ]Vin   ═║ U ║═               7[ ] ║══════> SIM800L tx
                                        ║          ═║ I ║═               6[ ]~║
                                        ║ [ ]A0    ═║ N ║═               5[ ]~║
                                        ║ [ ]A1    ═║ O ║═               4[ ] ║
                                        ║ [ ]A2     ╚═══╝           INT1/3[ ]~║
                                        ║ [ ]A3                     INT0/2[ ] ║══════> Interrupt pin for the "do" pin of the vibration sensor
                                        ║ [ ]A4/SDA  RST SCK MISO     TX>1[ ] ║
                                        ║ [ ]A5/SCL  [ ] [ ] [ ]      RX<0[ ] ║
                                        ║            [ ] [ ] [ ]              ║
                                        ║            GND MOSI 5V ╔════════════╝
                                        ╚═══UNO_R3═══════════════╝ 
*/
#include "Headers/messageHeader.h"
#include "Headers/messageAlert.h"
#include "Headers/messageTraget.h"
#include "Headers/messageHeartbeat.h"
#include "Headers/location.h"

//Server
#define SERVER_PHONE_NUMBER "+33769342048"  // BiKServer number (main server) called to get user number

//SIM 800L
#include <SoftwareSerial.h>                 // Software serial is used to comunicate with the sim800L.
#define PHONE_NUMBER "+33769342048"         // Device owner phone number TODO make it changable in the setup call SERVER_PHONE_NUMBER to get phone number
#define GSM_BAUDRATE 9600			        // Works because the sim800l baud rate is "hard coded" in the module.
#define GSM_RX 7					        // Declare the SIM800L onto the pins 7, 8.
#define GSM_TX 8					        // Declare the SIM800L onto the pins 7, 8.
#define STR_LENGTH 160				        // SMS lenght max 160 (one sms in limited in size !).

SoftwareSerial sim800l(GSM_RX, GSM_TX);     // Declare the SIM800L onto the pins 7, 8.


//GPS
location_t location;		                // Declare the Location type

//Vibration sensor
bool vibartion = false;                     // False most of the time but true if the module detected a vibration (trough interrupt)

#define VIBRATION 'V'

//Battery sensor
#define DEVICE_BATTERY_PIN  0               // Declare the device battery (analog)
#define BIKE_BATTERY_PIN  1	                // Declare the device battery (analog)

int deviceBatteryLevel = 0;
int bikeBatteryLevel = 0;

bool isBatteryCharging = false;

void setup()
{
	//SIM 800L
	sim800l.begin(9600);

	//Vibration sensor
	attachInterrupt(0, vibartionDetected, RISING); // Interrupt for the vibration detector (RISING because the detector emmit ~3.5V for 10 ms).

	//Serial communication (TODO delete every System.print(ln)();).
	Serial.begin(9600);


    /*
    Serial.begin(9600);
    Alert_msg_t alert_msg('V', -1.696969424269426942, 0.62115454426656874545216532, true, 42, 69);
    Serial.println("alert  message : ");
    Serial.println((char*) &alert_msg);
    
    Traget_msg_t traget_msg(-1.696969424269426942, 0.62115454426656874545216532, true, 42, 69, 150, 90);
    Serial.println("traget message : ");
    Serial.println((char*) &traget_msg);

    Heartbeat_msg_t heartbeat_msg(-1.696969424269426942, 0.62115454426656874545216532, true, 42, 69);
    Serial.println("traget message : ");
    Serial.println((char*) &heartbeat_msg);*/
}

void loop()
{
    if (vibartion)
	{
		noInterrupts();
		vibartion = false;
        actualizeLocation();
        actualizeDeviceBattery();
        actualizeBikeBattery();
		Alert_msg_t alert_msg(
            VIBRATION,
            location.longitude,
            location.latitude,
            isBatteryCharging,
            deviceBatteryLevel,
            bikeBatteryLevel
            );

            Serial.println((char*) &alert_msg);
            sendSMSTo((char*) &alert_msg);
		interrupts();
	}
    delay(1000);
    
}


void
actualizeLocation()
{
    //Nointerrupts later !!!!
    //TODO implement this ok!
    location.latitude = 0.62115455000000;
	location.longitude = 1.6969694000000000;
}


void
actualizeDeviceBattery()
{
    //TODO implement this ok!
    deviceBatteryLevel = 50;
}

void
actualizeBikeBattery()
{
    //TODO implement this ok!
    bikeBatteryLevel = 42;
}

void
actualizeIsBatteryCharging()
{
    isBatteryCharging = false;
}

void
vibartionDetected()
{
    vibartion = true; 
    Serial.println("moto a vibrationed");
}
