#include <DFRobot_sim808.h>
#include <sim808.h>

/*
  ### Starting code to use DFRobot_SIM808 GPS/GPRS/GSM Shield's with Leonardo card
  This example is used to test DFRobot_SIM808 GPS/GPRS/GSM Shield's GPS and
   reading/sending SMS function.


  create on 2018/11/20, version: 1.0
  by Emmanuel Melin
*/

#include <Arduino.h>
#include <avr/io.h>
//#include <avr/interrupt.h>
//#include <util/atomic.h>

#define SERVER // prendre soin d'activer  le #define GG_DEBUG dans le .h de  la lib IUTO_SIM808

#include <IUTO_sim808C.h>

#define mySerial Serial1

#define Powerkey 12      // PIN used to  wake up shield
#define SIM8008rate 9600 //only 9600 works... Why??
#define STR_LENGTH 160

// SEND VARIABLES
char data[STR_LENGTH];
char send_phone[9] = "0000000000";

// RECEIVE VARIABLES
char str[STR_LENGTH];
char receive_phone[10] = "0000000000";
char datetime[15];

IUTO_SIM808 sim808(&mySerial);

//******Program states
bool ledON = false;       //switch on led
bool ledOFF = false;      //switch off led*
volatile bool testSMS = false;
volatile int seconds = 0; //make it volatile because it is used inside the interrupt
volatile bool testSim808 = false;
unsigned char count = 1;

void setup()
{

//******** if arduino is connected to a PC *************
#ifdef SERVER
    Serial.begin(SIM8008rate); //does not need to be same rate than mySerial so may be changed to other values
    while (!Serial)
        ;
    GG_DEBUG_PRINTLN("Sim808 is connected to PC");
    wink(10, 50);
#endif

    pinMode(Powerkey, OUTPUT); // needed to wake up shield

    //******** communication to  shield 808 *************
    mySerial.begin(SIM8008rate);
    while (!mySerial)
        ;

    wink(10, 50);
    wink(count++, 500);

    //******** Initialize sim808 module *************
    ResetSim808(true); //try to wake up shield  ; true-> a SMS will be send at the end of this process

    sim808_clean_buffer(str, sizeof(str));

    myinterrupts(1); //1Hz
}

void (*resetFunc)(void) = 0; //declare reset function @ address 0

ISR(TIMER1_COMPA_vect) // timer compare interrupt service routine
{
    // Do every nbsec second
    seconds++;
    if (seconds > 4500)
    {
        testSim808 = true;
        seconds = 0;
    }
    else
    {
        if (seconds % 10 == 0)
        {
            testSMS = true;
        }
    }
}

//Main arduino loop

void loop()
{
    delay(1); //For USB stability ??

    if (testSim808)
    {
        GG_DEBUG_PRINTLN("Test if 808 is still OK");
        if (!sim808.testSIM808(20000, true))
        {
            GG_DEBUG_PRINTLN("Lost Connection, decide to reset 808... ");
            ResetSim808(true);
            GG_DEBUG_PRINTLN("reset done");
        }
        testSim808 = false;
    }

    if (testSMS)
    {
        wink(2, 500);
        GG_DEBUG_PRINTLN("testSMS");
        tryReadSMS();
        testSMS = false;
    }

    if (ledON)
    {
        digitalWrite(LED_BUILTIN, HIGH);
        ledON = false;
    }

    if (ledOFF)
    {
        digitalWrite(LED_BUILTIN, LOW);
        ledOFF = false;
    }

#ifdef SERVER
    treatinformationsfromPC();
#endif
}

void treatinformationsfromPC()
{
    int i = 0;
    while (i < 159)
    {
        char curr = (char)Serial.read();
        if (curr == ';') {
            break;
        }
        else
        {   
            data[i] = curr;
        }
        i++;
    }
    for (int j = 0; j <= 9; j++)
    {
        send_phone[j] = (char)Serial.read();
    }
    snprintf(data, STR_LENGTH, data);
    sim808.sendSMS(send_phone, data);
    sim808_clean_buffer(data, sizeof(data));
}

void tryReadSMS()
{
    if (sim808.readSMS(1, str, STR_LENGTH, receive_phone, datetime))
    {
        wink(10, 50);
        sim808.deleteAllSMS(7000); // Delete message to free memory, may be important not to saturate memory

        GG_DEBUG_PRINTLN("reading message");
        Serial.flush();
        Serial.print(str);
        Serial.print(';');
        Serial.println(receive_phone);
    }
    sim808_clean_buffer(str, sizeof(str));
}

void wink(int nb, int wait)
{
    for (int i = 0; i < nb; i++)
    {
        digitalWrite(LED_BUILTIN, LOW);
        delay(wait);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(wait);
    }
}

void myinterrupts(unsigned long frequency)
{                   // not less than 0.1 hz
    noInterrupts(); // disable all interrupts

    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1 = 0;

    //OCR1A = 625;    // 10ms
    //OCR1A =1250000;
    OCR1A = (unsigned long)(62500UL / frequency); // compare match register 16MHz/256/100Hz
                                                  // 16000000/256/100
                                                  //100Hz= 100/s =toutes les  0,01s = 10ms
                                                  // This value makes ISR execute every 10ms

    TCCR1B |= (1 << WGM12);  // CTC mode
    TCCR1B |= (1 << CS12);   // 256 prescaler
    TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt

    interrupts();
}

void ResetSim808(bool sendaSMS)
{

    //  //******** Initialize sim808 data rate but does not work with other values than 9600 :-( *************

    wink(count++, 500);

    GG_DEBUG_PRINTLN("Init 808");
    sim808.powerReset(Powerkey);

    wink(count++, 500);

    GG_DEBUG_PRINTLN("Init rate with 808");
    while (!sim808.rate(SIM8008rate))
        ;

    {
        GG_DEBUG_PRINTLN("Turn Rate");
        mySerial.flush();
        mySerial.begin(SIM8008rate);
        while (mySerial.available())
        {
            GG_DEBUG_PRINTLN("Purge");
            mySerial.read();
        }
        //delay(1000);
    }

    //******** Wait a connection to the shield establised *************
    while (!sim808.testSIM808(1000, false))
    {
        delay(1000);
        wink(1, 200);
    }

    sim808.deleteAllSMS(10000); // Delete message to free memory, may be important not to saturate memory
}