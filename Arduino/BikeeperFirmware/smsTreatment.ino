#include <string.h>

#include "Utils.hpp"

#define BETWEEN_SMS_DELAY 3000 // Delay between sent sms 

void treatSMS()
{
	short senderIndex = sms_buffer.indexOf("+33", 3);
	char senderNumber[13];

	sms_buffer.substring(senderNumber, senderIndex, senderIndex + 13);
	sms_buffer.replaceTo(senderIndex, 'a'); // Replace first number (sender number) '+' bu 'a' TODO delete useless
	sms_buffer.toLower();
	
	message_buffer.clear();

	if (arraysCompare(senderNumber, SERVER_PHONE_NUMBER) || arraysCompare(senderNumber, userPhoneNumber))
	{
		if (sms_buffer.indexOf("unpark", 4) != -1) // User sent unpark bike command
		{
			if (parked)
			{
				parked = false;

				sendSMSToUser(indexStringBikeUnparked);

				message_buffer.clear();

				smsFormatter.makeStateUpdateSms('+', 'B');
				sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
				sim800L.smartRead("+CMGS", 5, 1000);

				delay(BETWEEN_SMS_DELAY);

			}
			else
			{
				sendSMSToUser(indexStringBikeNotParked);
			}
		}
		else if (sms_buffer.indexOf("park", 4) != -1) // User sent park bike command
		{
			if (!parked)
			{
				if (!journey)
				{
					parked = true;

					Serial.println("on est la 1 -------------------------------");
					sendSMSToUser(indexStringBikeParked);
					Serial.println("on est la 2 -------------------------------");

					smsFormatter.clear();

					smsFormatter.makeStateUpdateSms('+', 'A');
					sim800L.send(userPhoneNumber, smsFormatter.getStorage());
					sim800L.smartRead("+CMGS", 5, 1000);

					delay(BETWEEN_SMS_DELAY);

					Serial.println("on est la 3 -------------------------------");
				}
				else
				{
					parked = true;
					journey = false;
					sendSMSToUser(indexStringJourneyStopedAndParked);

					smsFormatter.makeStateUpdateSms('+', 'D');
					sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
					sim800L.smartRead("+CMGS", 5, 1000);

					delay(BETWEEN_SMS_DELAY);

					smsFormatter.makeStateUpdateSms('+', 'A');
					sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
					sim800L.smartRead("+CMGS", 5, 1000);

					delay(BETWEEN_SMS_DELAY);

				}
			}
			else
			{
				sendSMSToUser(indexStringBikeAlreadyParked);
			}
		}

		else if (sms_buffer.indexOf("position", 8) != -1) // User sent position request command
		{
			/* TODO refactor using sms formatter */
			message_buffer.clear();

			message_buffer.store(StringCoordinatesStart);
			message_buffer.storeDouble(location.longitude, 16, 13);
			message_buffer.store(StringCoordinatesMiddle);
			message_buffer.storeDouble(location.latitude, 14, 12);

			sim800L.send(userPhoneNumber, message_buffer.getStorage());
			sim800L.smartRead("+CMGS", 5, 1000);
			delay(BETWEEN_SMS_DELAY);
		}

		else if (sms_buffer.indexOf("start", 5) != -1) // User sent start journey command
		{
			if (journey)
			{
				sendSMSToUser(indexStringJourneyStartedPleaseStop);
			}
			else
			{
				if (parked)
				{
					journey = true;
					parked = false;

					sendSMSToUser(indexStringJourneyStartedAndUnparked);
					
					smsFormatter.makeStateUpdateSms('+', 'B');
					sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
					sim800L.smartRead("+CMGS", 5, 1000);
					delay(BETWEEN_SMS_DELAY);

					smsFormatter.makeStateUpdateSms('+', 'C');
					sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
					sim800L.smartRead("+CMGS", 5, 1000);
					delay(BETWEEN_SMS_DELAY);
				}
				else
				{
					journey = true;

					sendSMSToUser(indexStringJourneyStarted);

					smsFormatter.makeStateUpdateSms('+', 'C');
					sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
					sim800L.smartRead("+CMGS", 5, 1000);
					delay(BETWEEN_SMS_DELAY);
				}
			}
		}
		else if (sms_buffer.indexOf("stop", 4) != -1) // User sent stop journey command
		{
			if (journey)
			{
				journey = false;

				sendSMSToUser(indexStringJourneyStopped);

				smsFormatter.makeStateUpdateSms('+', 'D');
				sim800L.send(SERVER_PHONE_NUMBER, smsFormatter.getStorage());
				sim800L.smartRead("+CMGS", 5, 1000);
				delay(BETWEEN_SMS_DELAY);
			}
			else
			{
				sendSMSToUser(indexStringJourneyNotStarted);
			}
		}
		else if (sms_buffer.indexOf("ok", 2) != -1) // User sent ok command
		{
			if (bikeFallen)
			{
				bikeFallen = false;
				fallTime = 0 ;

				sendSMSToUser(indexStringStringOkBeSafe);
			}
		}
	}
	message_buffer.clear();
}


void
sendSMSToUser(const short index)
{
	message_buffer.clear();

	strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[index])));
	sim800L.send(userPhoneNumber, message_buffer.getStorage());
	sim800L.smartRead("+CMGS", 5, 1000);

	delay(BETWEEN_SMS_DELAY);
}