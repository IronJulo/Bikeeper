#include "Utils.hpp"

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
				strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringBikeUnparked])));
				sim800L.send(userPhoneNumber, message_buffer.getStorage());
				delay(100);
				parked = false;
			}
			else
			{
				strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringBikeNotParked])));
				sim800L.send(userPhoneNumber,  message_buffer.getStorage());
				delay(100);
				parked = true;
			}
		}
		else if (sms_buffer.indexOf("park", 4) != -1) // User sent park bike command
		{
			if (!parked)
			{
				if (!journey)
				{
					strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringBikeParked])));
					sim800L.send(userPhoneNumber,  message_buffer.getStorage());
					delay(100);
					parked = true;
				}
				else
				{
					Serial.println("On est la on est ici ");
					strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringJourneyStopedAndParked])));
					sim800L.send(userPhoneNumber,  message_buffer.getStorage());
					delay(100);
					parked = true;
				}
			}
			else
			{
				strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringBikeAlreadyParked])));
				sim800L.send(userPhoneNumber,  message_buffer.getStorage());
				delay(100);
			}
		}

		else if (sms_buffer.indexOf("position", 8) != -1) // User sent position request command
		{
			/*TODO*/
		}

		else if (sms_buffer.indexOf("start", 5) != -1) // User sent start journey command
		{
			if (journey)
			{
				strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringJourneyStartedPleaseStop])));
				sim800L.send(userPhoneNumber,  message_buffer.getStorage());
				delay(100);
			}
			else
			{
				if (parked)
				{
					strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringJourneyStartedAndUnparked])));
					sim800L.send(userPhoneNumber,  message_buffer.getStorage());
					delay(100);
					journey = true;
					parked = false;
				}
				else
				{
					strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringJourneyStarted])));
					sim800L.send(userPhoneNumber,  message_buffer.getStorage());
					delay(100);
					journey = true;
				}
			}
		}
		else if (sms_buffer.indexOf("stop", 4) != -1) // User sent stop journey command
		{
			if (journey)
			{
				strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringJourneyStopped])));
				sim800L.send(userPhoneNumber,  message_buffer.getStorage());
				delay(100);
				journey = false;
			}
			else
			{
				strcpy_P(message_buffer.getStorage(), (char *)pgm_read_word(&(string_table[indexStringJourneyNotStarted])));
				sim800L.send(userPhoneNumber,  message_buffer.getStorage());
				delay(100);
			}
		}
	}
	message_buffer.clear();
}