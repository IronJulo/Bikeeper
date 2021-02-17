#include <Arduino.h>
#include <SoftwareSerial.h>
#include <string.h>

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"
#include "Utils.hpp"

#define SERVER_PHONE_NUMBER "+33769342048" // BiKServer number (main server) called to get user number

char userPhoneNumber[13] = "";

#define GSM_RX 7
#define GSM_TX 8

SoftwareSerial softwareSim800l(GSM_RX, GSM_TX);

char sms_storage[100];
StringBuffer sms_buffer(sms_storage, sizeof(sms_storage));

char message_storage[50];
StringBuffer message_buffer(message_storage, sizeof(message_storage));

I_Sim800L sim800L(&softwareSim800l, &sms_buffer);

// states
bool parked = false;
bool journey = false;

void setup()
{
	Serial.begin(9600);
	sim800L.init(userPhoneNumber, SERVER_PHONE_NUMBER);

	message_buffer.clear();
	strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringSyncOk])));
	sim800L.send(userPhoneNumber, message_buffer.getStorage());

	Serial.println(message_buffer.getStorage());
	message_buffer.clear();
	sim800L.smartRead("+CMGS", 5, 30000);
	sim800L.deleteALL();
	sim800L.setModeTexte();
	sim800L.smartRead("OK", 2, 500);
}

void loop()
{
	Serial.println("waiting command");
	Serial.println();
	sim800L.deleteALLRead();
	sim800L.carriageReturn();
	sim800L.setModeTexte();
	sim800L.carriageReturn();

	if (sim800L.smartRead("+CMTI", 5, 1000))
	{
		sim800L.setModeTexte();
        sim800L.carriageReturn();
        sim800L.smartRead("+CMTI", 5, 1000);
		Serial.println(sms_buffer.getStorage());
		treatSMS();
	}
}
