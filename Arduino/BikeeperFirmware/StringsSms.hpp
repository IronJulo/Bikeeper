#ifndef STRINGSMS_H
#define STRINGSMS_H

/* Program stored data*/
/* UI strings used to comunicate with user */

/* Envoyé quand on demarre le device */ /* None */
const char StringSyncOk[] PROGMEM = "Now sync with your device";
/* Envoyé quand on demande de "degarer" la moto et quelle etait garée */ /* unpark */
const char StringBikeUnparked[] PROGMEM = "Your Bike is now unparked";
/* Envoyé quand on demande de "degarer" la moto et quelle n'est pas garée*/ /* unpark */
const char StringBikeNotParked[] PROGMEM = "Your Bike is not parked";
/* Envoyé quand on demande de "degarer" la moto et quelle est garée et qu'on etair en "journey" */ /* unpark */
const char StringJourneyStopedAndParked[] PROGMEM = "We stopped your journey & your bike is now parked";
/* Envoyé quand on demande de garer la moto et quelle n'etait pas garée */ /* parked */
const char StringBikeParked[] PROGMEM = "Your bike is now parked";
/* Envoyé quand on demande de garer la moto et quelle est deja garée */ /* parked */
const char StringBikeAlreadyParked[] PROGMEM = "Your Bike is already parked";
/* Envoyé quand on demande de demarrer une journey et qu'une journey est deja demarrée */ /* start */
const char StringJourneyStartedPleaseStop[] PROGMEM = "Journey already started please stop it";
/* Envoyé quand on demande de demarrer une journey mais que la moto etait garée */ /* start */
const char StringJourneyStartedAndUnparked[] PROGMEM = "Journey started & your bike is now unparked";
/* Envoyé quand on demande de demarrer une journey */ /* start */
const char StringJourneyStarted[] PROGMEM = "Journey started ride safe";
/* Envoyé quand on demande de stoper une journey */ /* stop */
const char StringJourneyStopped[] PROGMEM = "Journey stoped";
/* Envoyé quand on demande de stoper une journey mais qu'aucune journey n'etait commencer */ /* stop */
const char StringJourneyNotStarted[] PROGMEM = "Journey not started you can start one";
/* Envoyé quand on detecte une vibration */ /* None */
const char StringVibrationDetected[] PROGMEM = "Vibration detected check your bike";
/* Envoyé quand on detecte que la moto a bouger */ /* None */
const char StringMovementDetected[] PROGMEM = "Bike movement detected check your bike";
/* Envoyé quand on detecte que la batterie est faible */ /* None */
const char StringLowBatteryDetected[] PROGMEM = "Low battery check your bike";
/* Envoyé quand on detecte une chute */ /* None */
const char StringFallDetected[] PROGMEM = "Fall detected are you fine ? \'Fine\'";
/* Envoyé quand on confirme que ca va apres une chute*/ /* Fine */
const char StringOkBeSafe[] PROGMEM = "Ok be safe";
/* debut sms de position */ /* None */
const char StringCoordinatesStart[] = "Pos \rLon :  ";
/* milieu sms de position */ /* None */
const char StringCoordinatesMiddle[] = "\rLat :  ";
/* Position */ /* (ca fait appel aux deux strings du dessus) */
/*
message recu quand on demande la position
Pos
lon: + 1.342284400000
lat: +48.066959000000
*/

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
	StringFallDetected,
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
