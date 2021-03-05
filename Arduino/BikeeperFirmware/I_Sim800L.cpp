#include <Arduino.h>
#include <SoftwareSerial.h>

#include "I_Sim800L.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"


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
    listen();
    
    Serial.println("Initialisation...");
    delay(10000);
    setModeAT();                                                             // Start to talk to the SIM800L
    smartRead("OK", 2, 1000);                                               // Wait for ok

    I_Sim800L::deleteALL();                                                  // Delete all sms received sent read unread
    smartRead("OK", 2, 1000);                                               // Wait for ok


    send(serverPhoneNumber, INIT_MESSAGE);

    smartRead("OK", 2, 1000); 


    m_softwareSerial->println("AT+CMGF=1");                                 // Mode Texte TODO delete
    m_softwareSerial->println("\r");
    m_stringBuffer->clear();                                                // Clear buffer 

    

    while (userPhoneNumber[0] != '+')                                       // While the user phone number as not been received
    {
        deleteALLRead();
        m_softwareSerial->println("\r");
        
        setModeTexte();
        m_softwareSerial->println("\r");

        if (smartRead("+CMTI", 5, 1000))                                    // If we have received an sms
        {
            setModeTexte();                                                // Set the sim800l to read
            m_softwareSerial->println("\r");
            smartRead("+CMTI", 5, 1000);                                    // Read sms (store it in the buffer)
            initTreatement(userPhoneNumber, serverPhoneNumber);             // Treat the received sms

        }
        Serial.println("waiting for server response");
    }
    
}

void 
I_Sim800L::send(const char *to, const char *msg)
{
    //noInterrupts();
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
    //interrupts();
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
    short senderIndex = m_stringBuffer->indexOf("+33", 3);
    if (senderIndex != -1){                                                                 //TODO 12 -> 13 

        m_stringBuffer->replaceTo(m_stringBuffer->indexOf("+33", 3), 'a');

        short index = m_stringBuffer->indexOf("+33", 3);
        if (index != -1){
            m_stringBuffer->substring(userPhoneNumber, index, index+12);
            userPhoneNumber[12] = '\0';
            Serial.println(userPhoneNumber);
        }
    }

} 

void 
I_Sim800L::setModeAT()
{
    m_softwareSerial->println("AT");
}

void 
I_Sim800L::deleteALL()
{
    m_softwareSerial->println("AT+CMGD=,4");
}

void 
I_Sim800L::deleteALLRead()
{
    m_softwareSerial->println("AT+CMGD=1,2");
}

void 
I_Sim800L::setModeTexte()
{
    m_softwareSerial->println("AT+CMGR=1");
}

void
I_Sim800L::carriageReturn()
{
    m_softwareSerial->println("\r");
}

/*bool
I_Sim800L::compareArrays(const char *left, const char *right)
{

}*/
