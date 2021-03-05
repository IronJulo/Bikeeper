#include <Arduino.h>

#include "SmsFormatter.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"
#include "Headers/location.h"

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
SmsFormatter::storeBikeAngle(const int angle)
{
	/* TODO store sign */
	m_stringBuffer->store(angle < 0 ? '-' : '+');
	m_stringBuffer->storeInt3(abs(angle));
}

void
SmsFormatter::setCoordinates(const location_t *location)
{
	setSeparator();
	m_stringBuffer->storeDouble(location->longitude * 0.001, 18, 17);
	setSeparator();
	setSeparator();
	m_stringBuffer->storeDouble(location->latitude * 0.001, 16, 15);

}


char *
SmsFormatter::getStorage()
{
	return m_stringBuffer->getStorage();
}

void
SmsFormatter::storebatt(const short batteryLevel)
{
	//setSeparator();
	m_stringBuffer->storeInt3(batteryLevel);
}



void 
SmsFormatter::makeJourneySms(const char schema,
					const location_t *location,
					const bool charging,
					const double devicebatteryLevel,
					const double bikebatteryLevel,
					const short speed,
					const double angle)
{
	clear();

	m_stringBuffer->store("[bk]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f');
	setSeparator();
	storebatt(devicebatteryLevel);
	setSeparator();
	storebatt(bikebatteryLevel);
	setSeparator();
	m_stringBuffer->storeInt3(speed);
	setSeparator();
	storeBikeAngle(angle);
	setSeparator();
}

void 
SmsFormatter::makeAlertSms(const char schema,
				  const char type,
				  const location_t *location,
				  const bool charging,
				  const double devicebatteryLevel,
				  const double bikebatteryLevel)
{
	clear();

	m_stringBuffer->store("[bk]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	m_stringBuffer->store(type);
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f');
	setSeparator();
	storebatt(devicebatteryLevel);
	setSeparator();
	storebatt(bikebatteryLevel);
	setSeparator();
}

void 
SmsFormatter::makeHeartbeatSms(const char schema,
					  const location_t *location,
					  const bool charging,
					  const double devicebatteryLevel,
					  const double bikebatteryLevel)
{
	clear();

	m_stringBuffer->store("[bk]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f');
	setSeparator();
	storebatt(devicebatteryLevel);
	setSeparator();
	storebatt(bikebatteryLevel);
	setSeparator();
}
void
SmsFormatter::makeStateUpdateSms(const char schema,
								 const char type)
{
	clear();

	m_stringBuffer->store("[bk]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	m_stringBuffer->store(type);
	setSeparator();
}