#include <SoftwareSerial.h>
SoftwareSerial sim800l(7, 8);

void setup()
{
  Serial.begin(9600);
  sim800l.begin(9600);
  Serial.println("Initializing..."); 
  delay(1000);
  sim800l.println("AT");
  updateSerial();
  sim800l.println("AT+CMGF=1");
  updateSerial();
  sim800l.println("AT+CNMI=1,2,0,0,0");
  updateSerial();
}

void loop()
{
  updateSerial();
}

void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    sim800l.write(Serial.read());
  }
  while(sim800l.available()) 
  {
    Serial.write(sim800l.read());
  }
}
