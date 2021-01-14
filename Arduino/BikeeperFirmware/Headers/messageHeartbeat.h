#ifndef MESSAGES_HEARTBEAT_H
#define MESSAGES_HEARTBEAT_H
#include "messageHeader.h"
#include "storer.h"

/**
 * @file messageHeartbeat.h
 */

/** @struct message Heartbeat
 * This struct is an message (an Heartbeat message) message beeing sent evry x second 
 * 
 * @var Alert_msg_t::header
 *      the message header
 * 
 * @var Alert_msg_t::_separator1-6
 *      the separators ";"
 * 
 * @var Alert_msg_t::schema
 *      the schema (to decode afterward in python)
 * 
 * @var Alert_msg_t::lon[19]
 *      the longitude
 * 
 * @var Alert_msg_t::lat[17]
 *      the latitude
 * 
 * @var Alert_msg_t::charging
 *      T/F if the batt is charging
 * 
 * @var Alert_msg_t::batteryLevel[3]
 *      the percent of charging of the battery 
 * 
 * @var Alert_msg_t::bikeBatteryLevel[3]
 *      the percent of charging of the bike battery
 * 
 * @var Alert_msg_t::speed[3]
 *      the speed of the bike
 * 
 * @var Alert_msg_t::angle[4]
 *      the speed of the bike
 */     

struct Heartbeat_msg_t
{
	header_t header;
	char _separator1;
	char lon[19];
    char _separator2;
	char lat[17];
	char _separator3;
	char charging;
	char _separator4;
	char batteryLevel[3];
	char _separator5;
	char bikeBatteryLevel[3];
    char _separator6;
	char _end;
    
    /**
     * Create the struct struct 
     * 
     */
    Heartbeat_msg_t(double lon, double lat, bool charging, int batteryLevel, int bikeBatteryLevel):
        header('*'),
        _separator1(';'),
        lon(),
        _separator2(';'),
        lat(),
        _separator3(';'),
        charging(charging ? 't': 'f'),
        _separator4(';'),
        batteryLevel(),
        _separator5(';'),
        bikeBatteryLevel(),
        _separator6(';'),
        _end('\0')
        {
            memcpy(this->lon, "+0.0000000000000000", sizeof(this->lon));
            memcpy(this->lat, "+0.0000000000000000", sizeof(this->lat));
            memcpy(this->batteryLevel, "000", sizeof(this->batteryLevel));
            memcpy(this->bikeBatteryLevel, "000", sizeof(this->bikeBatteryLevel));

            storeSignedDouble(lon, 18, 16, this->lon);
            storeSignedDouble(lat, 16, 14, this->lat);
            storeInt3(batteryLevel, this->batteryLevel);
            storeInt3(bikeBatteryLevel, this->bikeBatteryLevel);

        };


};


#endif