/* This code works with Sim800L and a push button
 * Press the button to send a simple SMS/Text to a specified phone number
 * Refer to www.SurtrTech.com for more details 
 */

#include <SoftwareSerial.h>

SoftwareSerial sim800l(2, 3); // RX,TX for the Arduino and for the module it's TXD RXD, they should be inverted

#define button1 4 //Button pin, on the other pin it's wired with GND

bool button_State; //Button state


void setup()
{
 
  pinMode(button1, INPUT_PULLUP); //The button is always on HIGH level, when pressed it goes LOW
  sim800l.begin(9600);   //Module baude rate, this is on max, it depends on the version
  Serial.begin(9600);   
  delay(1000);
}
 
void loop()
{
  

  button_State = digitalRead(button1);   //We are constantly reading the button State
 
  if (button_State == LOW) {            //And if it's pressed
    Serial.println("Button pressed");   //Shows this message on the serial monitor
    delay(200);                         //Small delay to avoid detecting the button press many times
    
    SendSMS();                          //And this function is called

 }
 
  if (sim800l.available()){            //Displays on the serial monitor if there's a communication from the module
    receivesms();
  }

  
}

 
void SendSMS()
{
  Serial.println("Sending SMS...");               //Show this message on serial monitor
  sim800l.print("AT+CMGF=1\r");                   //Set the module to SMS mode
  delay(100);
  sim800l.print("AT+CMGS=\"+33769342048\"\r");  //Your phone number don't forget to include your country code, example +212123456789"
  delay(100);
  sim800l.print("vous etes un humain a 100%");       //This is the text to send to the phone number, don't make it too long or you have to modify the SoftwareSerial buffer
  delay(100);
  sim800l.print((char)26);// (required according to the datasheet)
  delay(100);
  sim800l.println();
  Serial.println("Text Sent.");
  delay(100);

}



void GetLoc(){
  Serial.println("je gette ta position mamen ...."); 
  sim800l.print("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
  delay(100);
  sim800l.print("AT+SAPBR=3,1,\"APN\",\"your apn here\"");
  delay(100);
  sim800l.print("AT+SAPBR=1,1");
  delay(100);
  sim800l.print("AT+CIPGSMLOC=1,1");
  delay(100);
  Serial.println("dataatad");

}

void receivesms(){
  Serial.println("Receiving text message...");
  sim800l.print("AT+CMGF=1r");   // Configure le mode SMS
  // Affiche tous les messages
  sim800l.print("AT+CMGL=\"ALL\"r");
  delay(1000);
  sim800l.println();
}



 
