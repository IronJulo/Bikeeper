#ifndef __IUTO_SIM808_H__
#define __IUTO_SIM808_H__



#include <DFRobot_sim808.h>
#include <sim808.h>

/*!
 * @file IUTO_sim808.h
 * @n Header file for IUTO's SIM808 GPS/DFRobot_SIM808/GSM Shield
 *
 * @copyright	[IUTO](http://www.univ-orleans.fr/iut-orleans), 2018
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
 


/** IUTO_SIM808 class.
 *  used to realize IUTO_SIM808 communication
 */ 
 
#define GG_DEBUG

#ifdef GG_DEBUG
#define GG_DEBUG_PRINTLN(x) Serial.println(x);Serial.flush()
#else
#define GG_DEBUG_PRINTLN(x)
#endif

class IUTO_SIM808  : public DFRobot_SIM808
{
public:
    
  IUTO_SIM808(HardwareSerial *mySerial);
    bool init(unsigned int timeout);
    char isSMSread();
    bool readSMS(int messageIndex, char *message,int length, char *phone, char *datetime);

    bool deleteAllSMS();
    bool deleteAllSMS(int time);
  void powerReset(uint8_t pin); 
  bool rate(unsigned long rate);
  bool poweronGPS();
  bool poweroffGPS();
  bool readGPS();
    bool testSIM808(  int timeout, boolean debug) ;
  bool waitGPSready(unsigned long time);
      bool waitGPSready();
  bool readINFGPS();
    void getINFGPSDate(uint32_t date);
    void getINFGPSTime(uint32_t date);
  void latitudeConverToDegdec();
  void longitudeConverToDegdec();
    double distNewPosition(double oldlat, double oldlng);
    float latDec=0.0;
    float longDec=0.0;
    float speed_kmH=0.0;
      float lastmov=0.0;
  void printdataGPS();
};
#endif
