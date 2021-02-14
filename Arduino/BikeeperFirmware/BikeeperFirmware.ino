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
#include "Headers/messageHeader.h"
#include "Headers/messageAlert.h"
#include "Headers/messageTrajet.h"
#include "Headers/messageHeartbeat.h"
#include "Headers/messageReceived.h"
#include "Headers/location.h"

#include <TinyGPS++.h>

//Server
#define SERVER_PHONE_NUMBER "+33769342048"  // BiKServer number (main server) called to get user number

//SIM 800L
#include <SoftwareSerial.h>                 // need to be slightly modified to have a bigger buffer (100 instead of 64)
                                            // line 43 #define _SS_MAX_RX_BUFF 64
                                            // will become #define _SS_MAX_RX_BUFF 100
String userPhoneNumber;                     // Device owner phone number TODO make it changable in the setup call SERVER_PHONE_NUMBER to get phone number
#define GSM_BAUDRATE 9600			        // Works because the sim800l baud rate is "hard coded" in the module.
#define GSM_RX 7					        // Declare the SIM800L onto the pin 7.
#define GSM_TX 8					        // Declare the SIM800L onto the pin 8.
#define STR_LENGTH 160				        // SMS lenght max 160 (one sms in limited in size !).

SoftwareSerial sim800l(GSM_RX, GSM_TX);     // Declare the SIM800L onto the pins 7, 8.

String answer, SMS;
String senderPhoneNumber;
unsigned long t0;



//Vibration sensor
bool vibartion = false;                     // False most of the time but true if the module detected a vibration (trough interrupt)

#define VIBRATION 'V'

//Battery sensor
#define DEVICE_BATTERY_PIN  0               // Declare the device battery (analog)
#define BIKE_BATTERY_PIN  1	                // Declare the device battery (analog)

int deviceBatteryLevel = 0;
int bikeBatteryLevel = 0;

bool isBatteryCharging = false;


//State

bool parked = false;
bool journey = false;

//GPS
#define GPS_RX 4					        // Declare the SIM800L onto the pin 7.
#define GPS_TX 3	

#define GPS_BAUDRATE 9600
//TinyGPSPlus gps;

location_t location;		                // Declare the Location type
//SoftwareSerial gpsSerial(GPS_RX, GPS_TX);

void setup()
{
    Serial.begin(9600);

    //GPS 
    //gpsSerial.begin(GPS_BAUDRATE);
    //pinMode(13, OUTPUT);
    
	//SIM 800L
	sim800l.begin(9600);
    
    
    sim800l.listen();
	//Vibration sensor
	attachInterrupt(0, vibartionDetected, RISING); // Interrupt for the vibration detector (RISING because the detector emmit ~3.5V for 10 ms).
  
  initCard();
  LireSMS();                                                  // Si nouveau SMS disponible SIM800 envoie +CMTI:
    sim800l.println("AT+CMGD=1,2");
	message("OK", 1000, 0);
	sim800l.println("AT+CMGDA=DEL INBOX");
    message("OK", 1000, 0); 
}

/*static void smartDelay(unsigned long ms)
{
  gpsSerial.listen();
  unsigned long start = millis();
  do 
  {
    while (gpsSerial.available())
      gps.encode(gpsSerial.read());
  } while (millis() - start < ms);
  sim800l.listen();

}*/

void loop()
{
    /*gpsSerial.listen();
    double oldlat = gps.location.lat();
    double oldlon = gps.location.lng();
    sim800l.listen();*/

    
    if (parked){                                                // Only detect vibration if we arer parked
    if (vibartion)                                              // Vibration detected
	    {
		noInterrupts();                                         // Stop interrupt
		vibartion = false;
        actualizeLocation();                                    // Actualise the localisation 
        actualizeDeviceBattery();                               // Actualise the device battery 
        actualizeBikeBattery();                                 // Actualise the bike battery 
		Alert_msg_t alert_msg(                                  // Set the data
            VIBRATION,
            location.longitude,
            location.latitude,
            isBatteryCharging,
            deviceBatteryLevel,
            bikeBatteryLevel
            );
            sendSMSTo(userPhoneNumber, (char*) &alert_msg);     // Use the Struct fo the char[] 
		interrupts();                                           // Activate interrupt
	    }
    }
    if (message("+CMTI:", 1000, 1))
        {
        Serial.println(F("Maisage Recaivent-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"));
        LireSMS();                                                                                 // Si nouveau SMS disponible SIM800 envoie +CMTI:
        sim800l.println("AT+CMGD=1,2");

    	Serial.print(F("answer : "));
        Serial.println(answer);
        Serial.println();
        message("OK", 1000, 0); 
    	}
    //smartDelay(1000);
    //message("OK", 1000, 1);
	Serial.print(F("answer : "));
    Serial.println(answer);
	//sim800l.println("AT+CMGD=1,2");
	//message("OK", 1000, 0); 
}

void
actualizeLocation()
{
    //Nointerrupts later !!!!
    //TODO implement this ok!
    location.latitude = 0.0;//gps.location.lat();
	location.longitude = 0.0;//gps.location.lng();
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
    Serial.println(F("moto a vibrationed"));
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
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    for (int i=flen; i<len; ++i)
      Serial.print(' ');
  }
  delay(0);
}
