#ifndef MESSAGES_TRAJET_H
#define MESSAGES_TRAJET_H
#include "messageHeader.h"
#include "storer.h"

/**
 * @file messageTrajet.h
 */

/** @struct message Trajet
 * This struct is an message (for the Trajet heartbeat)
 * 
 * @var Traget_msg_t::header
 *      the message header
 * 
 * @var Traget_msg_t::_separator1-7
 *      the separators ";"
 *
 * @var Traget_msg_t::lon[19]
 *      the longitude
 * 
 * @var Traget_msg_t::lat[17]
 *      the latitude
 * 
 * @var Traget_msg_t::charging
 *      T/F if the batt is charging
 * 
 * @var Traget_msg_t::batteryLevel[3]
 *      the percent of charging of the battery 
 * 
 * @var Traget_msg_t::bikeBatteryLevel[3]
 *      the percent of charging of the bike battery
 * 
 * @var Traget_msg_t::speed[3]
 *      the speed of the bike
 * 
 * @var Traget_msg_t::angle[4]
 *      the speed of the bike
 */     

struct Traget_msg_t
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
	char speed[3];
    char _separator7;
	char angle[4];
    char _separator8;
	char _end;
    /**
     * Create the struct 
     * 
     */
    Traget_msg_t(double lon, double lat, bool charging, int batteryLevel, int bikeBatteryLevel, int speed, int angle):
        header('@'),
        _separator1(';'),
        lon(),
        _separator2(';'),
        lat(),
        _separator3(';'),
        charging(charging ? 'T': 'F'),
        _separator4(';'),
        batteryLevel(),
        _separator5(';'),
        bikeBatteryLevel(),
        _separator6(';'),
        speed(),
        _separator7(';'),
        angle(),
        _separator8(';'),
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
            storeInt3(speed, this->speed);
            storeSignedInt4(angle, this->angle);

        };


};


#endif