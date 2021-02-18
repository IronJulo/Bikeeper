#include <Arduino.h>

#include "SmsFormatter.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"

SmsFormatter::SmsFormatter(StringBuffer *stringBuffer) : m_stringBuffer(stringBuffer)
{
	m_stringBuffer->clear();
};

void SmsFormatter::clear()
{
	m_stringBuffer->clear();
}

void 
SmsFormatter::setSeparator()
{
	m_stringBuffer->store(';');
}

void 
SmsFormatter::setBikeAngle(const short angle)
{
	/* TODO */
	m_stringBuffer->store("+longitudeeeeeeeeee");
	setSeparator();
	m_stringBuffer->store("+latitudeeeeeeee");
}

void
SmsFormatter::setCoordinates(const location_t *location)
{
	/* TODO */
	m_stringBuffer->store(';');
}


char *
SmsFormatter::getStorage()
{
	return m_stringBuffer->getStorage();
}

void 
SmsFormatter::makeJourneySms(const char schema,
					const location_t *location,
					const bool charging,
					const short devicebatteryLevel,
					const short bikebatteryLevel,
					const short speed,
					const short angle)
{
	m_stringBuffer->store("[BK]");
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f'); //TODO See with Andrew t / T | f / F
	setSeparator();
	m_stringBuffer->store(devicebatteryLevel);
	setSeparator();
	m_stringBuffer->store(bikebatteryLevel);
	setSeparator();
	m_stringBuffer->store(speed);
	setSeparator();
	setBikeAngle(angle);
	setSeparator();
}
/*
void 
SmsFormatter::makeAlertSms(const char schema,
				  const char type,
				  const location_t *location,
				  const bool charging,
				  const short devicebatteryLevel,
				  const short bikebatteryLevel);

void 
SmsFormatter::makeHeartbeatSms(const char schema,
					  const location_t *location,
					  const bool charging,
					  const short devicebatteryLevel,
					  const short bikebatteryLevel);

void 
SmsFormatter::makeStateUpdateSms(const char schema,
						const char type);*/

/*void
SmsFormatter::makeUiPosSms(const location_t *location)
{
	m_stringBuffer->store((char *)pgm_read_word(&(string_table[indexStringCoordinatesStart])));
	m_stringBuffer->store("+longitudeeeeeeeeee");
	m_stringBuffer->store((char *)pgm_read_word(&(string_table[indexStringCoordinatesMiddle])));
	m_stringBuffer->store("+latitudeeeeeeee");
}*/

void
SmsFormatter::store(const char *arr)
{
	m_stringBuffer->store(arr);
}
