#include <Arduino.h>
#include <SoftwareSerial.h>

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"

#define SERVER_PHONE_NUMBER "+33769342048"  // BiKServer number (main server) called to get user number

char userPhoneNumber[13] = "";

#define GSM_RX 7
#define GSM_TX 8

SoftwareSerial sim800l(GSM_RX, GSM_TX);

char sms_storage[255];
StringBuffer sms_buffer(sms_storage, sizeof(sms_storage));
I_Sim800L sim800L(&sim800l, &sms_buffer);

void setup() 
{
  Serial.begin(9600);
  sim800L.init(userPhoneNumber, SERVER_PHONE_NUMBER);
}

void loop() 
{
  Serial.println("-*-*-*-*-*-*-*qDQSqdsQSDqsdSQDQSDQSDQS-*-*-*");
  if (sim800L.smartRead("+CMTI", 5, 1000)){
    Serial.println("smsreceived");
  }

  Serial.println("user phone number");
  Serial.println(userPhoneNumber);
  Serial.println();
}
