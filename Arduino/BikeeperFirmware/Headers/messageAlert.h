#ifndef MESSAGES_ALERT_H
#define MESSAGES_ALERT_H
#include "messageHeader.h"
#include "storer.h"

/**
 * @file messageAlert.h
 */

/** @struct message Alert
 * This struct is an message (an alert message)
 * 
 * @var Alert_msg_t::header
 *      the message header
 * 
 * @var Alert_msg_t::_separator1-6
 *      the separators ";"
 * 
 * @var Alert_msg_t::alertType
 *      the alertType (to decode afterward in python)
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
 */     

struct Alert_msg_t
{
	header_t header;
	char _separator1;
    char alertType;
    char _separator2;
	char lon[19];
	char _separator3;
	char lat[17];
	char _separator4;
	char charging;
	char _separator5;
	char batteryLevel[3];
	char _separator6;
	char bikeBatteryLevel[3];
    char _separator7;
	char _end;
    /**
     * Create the struct struct 
     * 
     */
    Alert_msg_t(char alertType, double lon, double lat, bool charging, int batteryLevel, int bikeBatteryLevel):
        header('W'),
        _separator1(';'),
        alertType(alertType),
        _separator2(';'),
        lon(),
        _separator3(';'),
        lat(),
        _separator4(';'),
        charging(charging ? 'T': 'F'),
        _separator5(';'),
        batteryLevel(),
        _separator6(';'),
        bikeBatteryLevel(),
        _separator7(';'),
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