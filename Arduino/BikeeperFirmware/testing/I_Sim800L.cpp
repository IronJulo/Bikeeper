#include <Arduino.h>
#include <SoftwareSerial.h>

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"

I_Sim800L::I_Sim800L(SoftwareSerial *serial, StringBuffer *stringBuffer) : 
    m_softwareSerial(serial),
    m_stringBuffer(stringBuffer)
{
    m_stringBuffer->clear();
};

void 
I_Sim800L::begin(unsigned int baudrate)
{
    m_softwareSerial->begin(baudrate);
}

void 
I_Sim800L::listen()
{
    m_softwareSerial->listen();
}

void 
I_Sim800L::init(char userPhoneNumber[], const char serverPhoneNumber[])
{
    m_stringBuffer->clear();
    begin(9600);
    listen();
    
    Serial.println("Initialisation...");

    m_softwareSerial->println("AT"); // Start to talk to the SIM800L
    smartRead("OK", 2, 1000);

    m_softwareSerial->println("AT+CMGD=,4");
    smartRead("OK", 2, 1000);

    m_softwareSerial->println("AT+CMGF=1"); // Mode Texte TODO delete
    m_softwareSerial->println("\r");
    m_stringBuffer->clear();

    while (userPhoneNumber[0] != '+')
    {
        m_softwareSerial->println("AT+CMGD=1,2");
        m_softwareSerial->println("\r");
        
        m_softwareSerial->println("AT+CMGR=1");    
        m_softwareSerial->println("\r");

        if (smartRead("+CMTI", 5, 1000))
        {
            m_softwareSerial->println("AT+CMGR=1");    
            m_softwareSerial->println("\r");
            smartRead("+CMTI", 5, 1000);
            initTreatement(userPhoneNumber, serverPhoneNumber);

        }
        Serial.println("user phone number");
        Serial.println(userPhoneNumber);
        Serial.println();
        
    }
    //m_softwareSerial->println("AT+CMGDA=1");
    //m_softwareSerial->println("AT+CMGDA=DEL ALL");

    smartRead("+CMGS", 5, 30000);
}

void 
I_Sim800L::send(const char *to, const char *msg)
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

bool 
I_Sim800L::smartRead(const char waiting[], short waitingSize, unsigned int timeout)
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
        if (m_stringBuffer->indexOf(waiting, waitingSize) != -1)
        {
            Serial.println("rien ne vas plus ");
            res = true;
            delay(100);
            while (m_softwareSerial->available())
            {
                m_stringBuffer->store(m_softwareSerial->read());
            }
            return (res);
        }
    }
    return (res);
}
void
I_Sim800L::initTreatement(char userPhoneNumber[], const char serverPhoneNumber[]){
    if (m_stringBuffer->indexOf(serverPhoneNumber, 12) != -1){    //TODO 12 -> 13 
        m_stringBuffer->replaceTo(m_stringBuffer->indexOf("+33", 3), 'a');

        short index = m_stringBuffer->indexOf("+33", 3);
        if (index != -1){
            m_stringBuffer->substring(userPhoneNumber, index, index+12);
        }
    }
} 