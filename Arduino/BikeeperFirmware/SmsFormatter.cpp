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
SmsFormatter::setBikeAngle(const short angle)
{
	/* TODO */
	m_stringBuffer->store("+ang");
}

void
SmsFormatter::setCoordinates(const location_t *location)
{
	setSeparator();
	m_stringBuffer->storeDouble(location->longitude * 0.001, 18, 17);
	setSeparator();
	setSeparator();
	m_stringBuffer->storeDouble(location->latitude * 0.01, 16, 15);

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
					const signed short angle)
{
	clear();

	m_stringBuffer->store("[BK]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f');
	setSeparator();
	m_stringBuffer->storeInt3(devicebatteryLevel);
	setSeparator();
	m_stringBuffer->storeInt3(bikebatteryLevel);
	setSeparator();
	m_stringBuffer->storeInt3(speed);
	setSeparator();
	m_stringBuffer->storeInt3(bikebatteryLevel);
	setBikeAngle(angle);
	setSeparator();
}

void 
SmsFormatter::makeAlertSms(const char schema,
				  const char type,
				  const location_t *location,
				  const bool charging,
				  const short devicebatteryLevel,
				  const short bikebatteryLevel)
{
	clear();

	m_stringBuffer->store("[BK]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	m_stringBuffer->store(type);
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f');
	setSeparator();
	m_stringBuffer->storeInt3(devicebatteryLevel);
	setSeparator();
	m_stringBuffer->storeInt3(bikebatteryLevel);
	setSeparator();
}

void 
SmsFormatter::makeHeartbeatSms(const char schema,
					  const location_t *location,
					  const bool charging,
					  const short devicebatteryLevel,
					  const short bikebatteryLevel)
{
	clear();

	m_stringBuffer->store("[BK]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	setCoordinates(location);
	setSeparator();
	m_stringBuffer->store(charging ? 't' : 'f');
	setSeparator();
	m_stringBuffer->storeInt3(devicebatteryLevel);
	setSeparator();
	m_stringBuffer->storeInt3(bikebatteryLevel);
	setSeparator();
}
void
SmsFormatter::makeStateUpdateSms(const char schema,
								 const char type)
{
	clear();

	m_stringBuffer->store("[BK]");
	setSeparator();
	m_stringBuffer->store(schema);
	setSeparator();
	m_stringBuffer->store(type);
	setSeparator();
}