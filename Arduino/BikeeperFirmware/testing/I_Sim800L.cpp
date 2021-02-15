#include <Arduino.h>
#include <SoftwareSerial.h>

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"

I_Sim800L::I_Sim800L(SoftwareSerial *serial, StringBuffer *stringBuffer) : m_softwareSerial(serial),
                                                                           m_stringBuffer(stringBuffer)
{
    m_stringBuffer->clear();
};

void I_Sim800L::init()
{
    m_stringBuffer->clear();
    m_softwareSerial->begin(9600);
    m_softwareSerial->listen();

    Serial.println("Initialisation...");

    m_softwareSerial->println("AT"); // Start to talk to the SIM800L
    smartRead("OK", 1000);

    m_softwareSerial->println("AT+CMGD=,4");
    smartRead("OK", 1000);
    m_softwareSerial->println("\r");
    m_softwareSerial->println("AT+CMGD=1,2");
    m_softwareSerial->println("\r");
    smartRead("OK", 1000);

    m_softwareSerial->println("AT+CMGF=1"); // Mode Texte TODO delete
    smartRead("OK", 1000);                  // Wait for the SIM800L to return "OK" for stability
    m_softwareSerial->println("AT+CMGR=1");
    m_softwareSerial->println("\r"); // Only read the first sms on the sim card!
    smartRead("OK", 1000);

    while ("" == "")
    {
        m_softwareSerial->println("AT+CMGD=1,2");
        m_softwareSerial->println((char)26);
        //smartRead("OK", 1000);
        
        m_softwareSerial->println("AT+CMGR=1");    
        m_softwareSerial->println((char)26);

        m_stringBuffer->clear();


        if (smartRead("+CMTI", 2000))
        {
            Serial.println("nada -*-*-*-*-*-*-*-*-*-*-*");
            m_softwareSerial->println("AT+CMGD=1,2");
            m_softwareSerial->println("\r");
            Serial.print(F("answer : "));
            Serial.println(m_stringBuffer->getStorage());
            Serial.println();
        }
        Serial.print(F("answer : "));
        Serial.println(m_stringBuffer->getStorage());
        Serial.println();
    }
    m_softwareSerial->println("AT+CMGDA=1");
    m_softwareSerial->println("AT+CMGDA=DEL ALL");

    smartRead("+CMGS", 30000);
}

void I_Sim800L::send(const char *to, const char *msg)
{
    noInterrupts();
    Serial.println("Sending SMS...");
    sendCommand("AT+CMGF=1\r");
    delay(1000);
    sendCommand("AT+CMGS=\"");
    sendCommand(to);
    sendCommand("\"\r");
    delay(1000);
    sendCommand(msg);
    sendCommand((char)26);
    sendCommand('\n');
    Serial.println("Text Sent.");
    interrupts();
}

void I_Sim800L::readii(unsigned int timeout)
{
    m_stringBuffer->clear();
    long t0 = millis();
    while (millis() - t0 < timeout)
    {
        while (m_softwareSerial->available())
            m_stringBuffer->store(m_softwareSerial->read());
    }
}

bool I_Sim800L::smartRead(const char waiting, unsigned int timeout)
{
    bool res = false;
    m_stringBuffer->clear();
    
    long t0 = millis();
    while (millis() - t0 < timeout)
    {
        while (m_softwareSerial->available())
        {
            m_stringBuffer->store(m_softwareSerial->read());
        }
        if (strstr(m_stringBuffer->getStorage(), "+CMTI"))
        {
            Serial.println("rien ne vas plus ");
            res = true;
            delay(100);
            while (m_softwareSerial->available())
            {
                m_stringBuffer->store(m_softwareSerial->read());
            }
            break;
        }
    }
    return (res);
}
