#ifndef MESSAGES_RECEIVED_H
#define MESSAGES_RECEIVED_H
#include "messageHeader.h"
#include "storer.h"
/*+CMT: "+33769342048","","21/01/15,01:45:03+04"
oui*/


struct Received_msg_t
{
	char atCommand[6];     //+CMT: //
    char _separator1;      //"//
	char phoneNumber[12];  //+33769342048//
	char _separator2;      //"//
    char _separator3;      //,//
    char _separator4;      //"//
    char _separator5;      //"//
    char _separator6;      //,//
    char _separator7;      //"//
	char dateMess[8];      //21/01/15//
	char _separator8;      //,//
	char hour[5];          //01:45//
	char _separator9;      //://
    char second[5];        //03+04//
    char _separator10;      //"//
    char _end;             //\0// 6+1+12+6+8+1+5+1+5+1+1=47
	char message[53];
    
    /**
     * Create the struct struct 
     * 
     */
    Received_msg_t(double lon, double lat, bool charging, int batteryLevel, int bikeBatteryLevel):
        atCommand(),     //+CMT: //
        _separator1(),      //"//
        phoneNumber(),  //+33769342048//
        _separator2(),      //"//
        _separator3(),      //,//
        _separator4(),      //"//
        _separator5(),      //"//
        _separator6(),      //,//
        _separator7(),      //"//
        dateMess(),      //21/01/15//
        _separator8(),      //,//
        hour(),          //01:45//
        _separator9(),      //://
        second(),        //03+04//
        _separator10(),      //"//
        _end(),             //\0// 6+1+12+6+8+1+5+1+5+1+1=47
        message()
        {

        };


};


#endif