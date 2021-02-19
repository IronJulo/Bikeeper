#ifndef STRINGSMS_H
#define STRINGSMS_H

/* Programme stored data*/
/* UI strings used to comunicate with user */
const char StringSyncOk[] PROGMEM = "Now sync with your device";
const char StringBikeUnparked[] PROGMEM = "Your Bike is now unparked";
const char StringBikeNotParked[] PROGMEM = "Your Bike is not parked";
const char StringJourneyStopedAndParked[] PROGMEM = "We stopped your journey & your bike is now parked";
const char StringBikeParked[] PROGMEM = "Your bike is now parked";
const char StringBikeAlreadyParked[] PROGMEM = "Your Bike is already parked";
const char StringJourneyStartedPleaseStop[] PROGMEM = "Journey already started please stop it";
const char StringJourneyStartedAndUnparked[] PROGMEM = "Journey started & your bike is now unparked";
const char StringJourneyStarted[] PROGMEM = "Journey started ride safe";
const char StringJourneyStopped[] PROGMEM = "Journey stoped";
const char StringJourneyNotStarted[] PROGMEM = "Journey not started you can start one";
const char StringVibrationDetected[] PROGMEM = "Vibration detected check your bike";
const char StringMovementDetected[] PROGMEM = "Bike movement detected check your bike";
const char StringLowBatteryDetected[] PROGMEM = "Low battery check your bike";
const char StringFallDetected[] PROGMEM = "Fall detected are you fine ? \'OK\'";
const char StringOkBeSafe[] PROGMEM = "Ok be safe";
const char StringCoordinatesStart[] = "Pos \rLon :  ";
const char StringCoordinatesMiddle[] = "\rLat :  ";

const short indexStringSyncOk PROGMEM = 0;
const short indexStringBikeUnparked PROGMEM = 1;
const short indexStringBikeNotParked PROGMEM = 2;
const short indexStringJourneyStopedAndParked PROGMEM = 3;
const short indexStringBikeParked PROGMEM = 4;
const short indexStringBikeAlreadyParked PROGMEM = 5;
const short indexStringJourneyStartedPleaseStop PROGMEM = 6;
const short indexStringJourneyStartedAndUnparked PROGMEM = 7;
const short indexStringJourneyStarted PROGMEM = 8;
const short indexStringJourneyStopped PROGMEM = 9;
const short indexStringJourneyNotStarted = 10;
const short indexStringVibrationDetected = 11;
const short indexStringMovementDetected = 12;
const short indexStringLowBatteryDetected = 13;
const short indexStringFallDetected = 14;
const short indexStringStringOkBeSafe = 15;


const char *const string_table[] PROGMEM = {
	StringSyncOk,
	StringBikeUnparked,
	StringBikeNotParked,
	StringJourneyStopedAndParked,
	StringBikeParked,
	StringBikeAlreadyParked,
	StringJourneyStartedPleaseStop,
	StringJourneyStartedAndUnparked,
	StringJourneyStarted,
	StringJourneyStopped,
	StringJourneyNotStarted,
	StringVibrationDetected,
	StringMovementDetected,
	StringLowBatteryDetected,
	StringOkBeSafe
	};

/* Ram Stored strings*/
/*
UI strings used to comunicate with user */
/*#define StringSyncOk "Now sync with your device"
#define StringBikeUnparked "Your Bike is now unparked"
#define StringBikeNotParked "Your Bike is not parked"
#define StringJourneyStopedAndParked "We stopped your journey & your bike is now parked"
#define StringBikeParked "Your bike is now parked"
#define StringBikeAlreadyParked "Your Bike is already parked"
#define StringJourneyStartedPleaseStop "Journey already started please stop it"
#define StringJourneyStartedAndUnparked "Journey started & your bike is now unparked"
#define StringJourneyStarted "Journey started ride safe"
#define StringJourneyStopped "Journey stoped"
#define StringJourneyNotStarted "Journey not started you can start one"*/

/* Protocols messages (not all some are built)  */
#define INIT_MESSAGE "[bk];I;"

#endif
