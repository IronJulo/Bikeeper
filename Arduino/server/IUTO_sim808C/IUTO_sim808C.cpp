/*!
 * @file IUTO_sim808.h
 * @n Header file for IUTO's SIM808 GPS/DFRobot_SIM808/GSM Shield
 *
 * @copyright    [IUTO](http://www.univ-orleans.fr/iut-orleans), 2018
 *
 * @author [Melin](emmanuel.melin@univ-orleans.fr)
 * @version  V1.0
 * @date  2018-09-15
 
 * The MIT License (MIT)
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */


#include <stdio.h>
#include "IUTO_sim808C.h"

extern Stream *serialSIM808;


IUTO_SIM808::IUTO_SIM808(HardwareSerial *mySerial):DFRobot_SIM808(mySerial){
    
};


//String sendData(String command, const int timeout, boolean debug) {
//    response = "";
//    serialSIM808->println(command);
//    serialSIM808->flush();
//    delay(5);
//    long int time = millis();
//    while( (time+timeout) > millis()){
//        while(serialSIM808->available()){
//            response += char(serialSIM808->read());
//        }
//    }
//    //if (debug) Serial.print(response);
//    return response;
//}
//
//bool sendData(String command,const char* resp, const int timeout, boolean debug) {
//
//
//    serialSIM808->println(command);
//    serialSIM808->flush();
//    delay(5);
//    int len = strlen(resp);
//    int sum = 0;
//    long int time = millis();
//    while( ((time+timeout) > millis())  ){
//        while(serialSIM808->available()){
//            char c = serialSIM808->read();
//            response += c;
//            sum = (c==resp[sum]) ? sum+1 : 0;
//            if(sum == len)goto end;
//        }
//
//    }
//end:
//    //if (debug) {Serial.print("Response:");Serial.print(response);Serial.flush();}
//    return (sum == len);
//}

bool IUTO_SIM808::init(unsigned int timeout)
{
    //閿熸枻鎷烽敓绱窽鎸囬敓鏂ゆ嫹閿熻鍑ゆ嫹閿熸枻鎷锋晥
    if(!sim808_check_with_cmd("AT\r\n","OK\r\n",CMD)){
        GG_DEBUG_PRINTLN("fail AT OK");
        return false;
        
    }
    //閿熸枻鎷烽敓绲奍M閿熻鍑ゆ嫹閿熸枻鎷锋簮閿熺晫璇濋敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷�
    // 1 : OK
    if(!sim808_check_with_cmd("AT+CFUN=1\r\n","OK\r\n",CMD)){
         GG_DEBUG_PRINTLN("fail AT+CFUN=1");
        return false;
    }
    
    //閿熸枻鎷烽敓绲奍M閿熸枻鎷风姸鎬�
    if(!checkSIMStatus()) {
        GG_DEBUG_PRINTLN("fail checkSIMStatus");
        return false;
    }
    return true;
}


bool IUTO_SIM808::readSMS(int messageIndex, char *message,int length, char *phone, char *datetime)
{
    /* Response is like:
  AT+CMGR=2
  
  +CMGR: "REC READ","XXXXXXXXXXX","","14/10/09,17:30:17+08"
  SMS text here
  
  So we need (more or lees), 80 chars plus expected message length in buffer. CAUTION FREE MEMORY
  */

    int i = 0;
    char gprsBuffer[80 + length];
    //char cmd[16];
	char num[4];
    char *p,*p2,*s;
    
    sim808_check_with_cmd("AT+CMGF=1\r\n","OK\r\n",CMD);
    delay(1000);
	//sprintf(cmd,"AT+CMGR=%d\r\n",messageIndex);
    //sim808_send_cmd(cmd);
	sim808_send_cmd("AT+CMGR=");
	itoa(messageIndex, num, 10);
	sim808_send_cmd(num);
	sim808_send_cmd("\r\n");
    sim808_clean_buffer(gprsBuffer,sizeof(gprsBuffer));
    sim808_read_buffer(gprsBuffer,sizeof(gprsBuffer));
      
    if(NULL != ( s = strstr(gprsBuffer,"+CMGR:"))){
        // Extract phone number string
        p = strstr(s,",");
        p2 = p + 2; //We are in the first phone number character
        p = strstr((char *)(p2), "\"");
        if (NULL != p) {
            i = 0;
            while (p2 < p) {
                phone[i++] = *(p2++);
            }
            phone[i] = '\0';            
        }
        // Extract date time string
        p = strstr((char *)(p2),",");
        p2 = p + 1; 
        p = strstr((char *)(p2), ","); 
        p2 = p + 2; //We are in the first date time character
        p = strstr((char *)(p2), "\"");
        if (NULL != p) {
            i = 0;
            while (p2 < p) {
                datetime[i++] = *(p2++);
            }
            datetime[i] = '\0';
        }        
        if(NULL != ( s = strstr(s,"\r\n"))){
            i = 0;
            p = s + 2;
            while((*p != '\r')&&(i < length-1)) {
                message[i++] = *(p++);
            }
            message[i] = '\0';
        }
        return true;
    }
    return false; 
}

char IUTO_SIM808::isSMSread()
{
    char gprsBuffer[48];  //48 is enough to see +CMGL:
    char *s;
    
    sim808_check_with_cmd("AT+CMGF=1\r\n","OK\r\n",CMD);
    //delay(1000);
    
    //List of all UNREAD SMS and DON'T change the SMS UNREAD STATUS
    sim808_send_cmd(F("AT+CMGL=\"REC READ\",1\r\n"));
    /*If you want to change SMS status to READ you will need to send:
     AT+CMGL=\"REC UNREAD\"\r\n
     This command will list all UNREAD SMS and change all of them to READ
     
     If there is not SMS, response is (30 chars)
     AT+CMGL="REC UNREAD",1  --> 22 + 2
     --> 2
     OK                      --> 2 + 2
     
     If there is SMS, response is like (>64 chars)
     AT+CMGL="REC UNREAD",1
     +CMGL: 9,"REC UNREAD","XXXXXXXXX","","14/10/16,21:40:08+08"
     Here SMS text.
     OK
     
     or
     
     AT+CMGL="REC UNREAD",1
     +CMGL: 9,"REC UNREAD","XXXXXXXXX","","14/10/16,21:40:08+08"
     Here SMS text.
     +CMGL: 10,"REC UNREAD","YYYYYYYYY","","14/10/16,21:40:08+08"
     Here second SMS
     OK
     */
    
    sim808_clean_buffer(gprsBuffer,31);
    sim808_read_buffer(gprsBuffer,30,DEFAULT_TIMEOUT);
    //Serial.print("Buffer isSMSunread: ");Serial.println(gprsBuffer);
    
    if(NULL != ( s = strstr(gprsBuffer,"OK"))) {
        //In 30 bytes "doesn't" fit whole +CMGL: response, if recieve only "OK"
        //    means you don't have any UNREAD SMS
        delay(50);
        return 0;
    } else {
        //More buffer to read
        //We are going to flush serial data until OK is recieved
        sim808_wait_for_resp("OK\r\n", CMD);
        //sim808_flush_serial();
        //We have to call command again
        sim808_send_cmd("AT+CMGL=\"REC READ\",1\r\n");
        sim808_clean_buffer(gprsBuffer,48);
        sim808_read_buffer(gprsBuffer,47,DEFAULT_TIMEOUT);
        //Serial.print("Buffer isSMSunread 2: ");Serial.println(gprsBuffer);
        if(NULL != ( s = strstr(gprsBuffer,"+CMGL:"))) {
            //There is at least one UNREAD SMS, get index/position
            s = strstr(gprsBuffer,":");
            if (s != NULL) {
                //We are going to flush serial data until OK is recieved
                sim808_wait_for_resp("OK\r\n", CMD);
                return atoi(s+1);
            }
        } else {
            return -1;
            
        }
    }
    return -1;
}


bool IUTO_SIM808::deleteAllSMS()  //blocking version
{
    
    
    
    sim808_send_cmd("AT+CMGDA=\"DEL ALL\"\r\n"); //MELIN
    
    return sim808_check_with_cmd("\r","OK\r\n",CMD);
}

bool IUTO_SIM808::deleteAllSMS(int time){ //unblocking version
    
    return sim808_check_with_cmd("AT+CMGDA=\"DEL ALL\"\r\n","OK\r\n",CMD);
    
    //return sendData("AT+CMGDA=\"DEL ALL\"","OK", time, false);
}



void IUTO_SIM808::powerReset(uint8_t pin)
{
    // reset for SIM808L board.
    // RST pin has to be OUTPUT, HIGH
    digitalWrite(pin,LOW);
    delay(1000);   //do not touch very tricky
    digitalWrite(pin,HIGH);
    delay(1000);//do not touch very tricky
    digitalWrite(pin,LOW);
    delay(1000);//do not touch very tricky
}

bool IUTO_SIM808::poweronGPS(){
 //   if(!sim808_check_with_cmd("AT+CGNSPWR=1\r\n", "OK\r\n", CMD,3000,1000)) {
        if(!sim808_check_with_cmd("AT+CGNSPWR=1\r\n", "OK\r\n",CMD)) {
            
        GG_DEBUG_PRINTLN("fail to power ON");
        return false;
    }
    GG_DEBUG_PRINTLN("Success power ON");
    return true;
}
bool IUTO_SIM808::poweroffGPS(){
    if(!sim808_check_with_cmd("AT+CGNSPWR=0\r\n", "OK\r\n", CMD)) {
        return false;
    }
    GG_DEBUG_PRINTLN("Success power OFF");
    return true;
}

bool IUTO_SIM808::readGPS(){
    return readINFGPS();
    
}

bool IUTO_SIM808::waitGPSready(unsigned long time){
    //    unsigned long start = millis();
    //    while ((!(ok)) && ((millis()-start)<time) ){
    int i=0;
    while ((!(readINFGPS())) && (i++<time) );
    return (i<time);
    
}


bool IUTO_SIM808::waitGPSready(){
    
    while (!readINFGPS()){
        delay(4000);
    }
    
    return true;
    
}

bool IUTO_SIM808::testSIM808(  int timeout, bool debug) {
    
    return sim808_check_with_cmd(F("AT\r\n"),"OK\r\n",CMD);
    
}


bool IUTO_SIM808::readINFGPS(){
    
    unsigned char ind[20];
    bool ok;
    
    int i = 0;
    char gprsBuffer[200];
    char buffer[20];
    char *s;
    
    sim808_flush_serial();
    sim808_send_cmd("AT+CGNSINF\r");
    sim808_clean_buffer(gprsBuffer,sizeof(gprsBuffer));
    sim808_read_buffer(gprsBuffer,sizeof(gprsBuffer),1,6*DEFAULT_INTERCHAR_TIMEOUT);
     GG_DEBUG_PRINTLN(gprsBuffer); //echo of characters
    if(NULL != ( s = strstr(gprsBuffer,"+CGNSINF:"))){
        String response=String(gprsBuffer);
        ind[0] = response.indexOf(',');  //finds location of first ,
        String field = response.substring(0, ind[0]);   //captures first data String
        for(int j=1;j<=19;j++)
            ind[j] = response.indexOf(',', ind[j-1]+1 );   //finds location of second ,
        
        uint32_t newDate = response.substring(ind[1]+1, ind[1]+9).toInt();
        getINFGPSDate(newDate);
        
        uint32_t newTime = response.substring(ind[1]+9, ind[1]+16).toInt();
        getINFGPSTime(newTime);
        
        float latDecProv = response.substring(ind[2]+1, ind[3]).toFloat();
        float longDecProv = response.substring(ind[3]+1, ind[4]).toFloat();
        float speed_kmHProv = response.substring(ind[5]+1, ind[6]).toFloat();
        
        if ((latDecProv>-90.0)  && (latDecProv<90.0) && (longDecProv>-180.0)  && (longDecProv<180.0) && ((latDecProv!=0.0)  || (longDecProv!=0.0) )){
            
            lastmov=distNewPosition(latDecProv,  longDecProv);
            latDec = latDecProv;
            longDec = longDecProv;
            speed_kmH = speed_kmHProv;
            return true;
        }
    }
    return false;
}

void IUTO_SIM808::getINFGPSDate(uint32_t date){
    GPSdata.year = date /10000;
    GPSdata.month  = (date /100) % 100;
    GPSdata.day = (date) % 100;
}

void IUTO_SIM808::getINFGPSTime(uint32_t time){
    GPSdata.hour     =  time / 10000;
    GPSdata.minute  = (time / 100) % 100;
    GPSdata.second = time  % 100;
    
}

void IUTO_SIM808::latitudeConverToDegdec()
{
    
    latDec = (int)GPSdata.lat;
    latDec += (GPSdata.lat - latDec)*10/6;
    
}

void IUTO_SIM808::longitudeConverToDegdec()
{
    longDec = (int)GPSdata.lon;
    longDec += (GPSdata.lon - longDec)*10/6;
    
}

#define LOCAL_PI 3.1415926535897932385

double ToRadians(double degrees)
{
    double radians = degrees * LOCAL_PI / 180;
    return radians;
}

double DirectDistance(double lat1, double lng1, double lat2, double lng2)
{
    double earthRadius = 3958.75;
    double dLat = ToRadians(lat2-lat1);
    double dLng = ToRadians(lng2-lng1);
    double a = sin(dLat/2) * sin(dLat/2) +
    cos(ToRadians(lat1)) * cos(ToRadians(lat2)) *
    sin(dLng/2) * sin(dLng/2);
    double c = 2 * atan2(sqrt(a), sqrt(1-a));
    double dist = earthRadius * c;
    double meterConversion = 1609.00;
    return dist * meterConversion;
}

double IUTO_SIM808::distNewPosition(double oldlat, double oldlng){
    return DirectDistance(oldlat,  oldlng,latDec,longDec);
}



bool IUTO_SIM808::rate(unsigned long rate){
    //serialSIM808->flush();
    delay(2);

    char str[120];
    snprintf (str,120, "AT+IPR=%lu\r\n",rate);
    Serial.print(str);
    if(!sim808_check_with_cmd(str, "OK\r\n", CMD)) { Serial.print("AT+IPR error ");
        return false;}
    delay(2);
    return true;
    
}

void IUTO_SIM808::printdataGPS(){
    char str[200];
    char str_temp_lat[30];
    dtostrf(latDec, 9, 6, str_temp_lat);
    
    char str_temp_lon[30];
    dtostrf(longDec, 9, 6, str_temp_lon);
    
    char str_temp_spd[30];
    dtostrf(speed_kmH, 9, 6, str_temp_spd);
    snprintf (str,200, "%u/%u/%u:%u:%u:%u::Lat:%s  Lon:%s  Vitesse:%s", GPSdata.day, GPSdata.month, GPSdata.year, GPSdata.hour, GPSdata.minute, GPSdata.second, str_temp_lat, str_temp_lon, str_temp_spd);
    // str is composed
    
    
    Serial.println(str);
    //Serial.flush();
}


