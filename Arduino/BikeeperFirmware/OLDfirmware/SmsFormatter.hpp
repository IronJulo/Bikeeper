#ifndef SMSFORMATTER_H
#define SMSFORMATTER_H

class SoftwareSerial;
class StringBuffer;
struct location_t;

class SmsFormatter
{
private:
	StringBuffer *m_stringBuffer;

public:
	SmsFormatter(StringBuffer *StringBuffer);

	void clear();
	void setMagic();
	void setCoordinates(const location_t *location);
	void setBikeAngle(const short angle);
	void setSeparator();

	void store(const char *arr);

	char *getStorage();

	void makeJourneySms(const char schema,
						const location_t *location,
						const bool charging,
						const short devicebatteryLevel,
						const short bikebatteryLevel,
						const short speed,
						const short angle);

	void makeAlertSms(const char schema,
					  const char type,
					  const location_t *location,
					  const bool charging,
					  const short devicebatteryLevel,
					  const short bikebatteryLevel);

	void makeHeartbeatSms(const char schema,
						  const location_t *location,
						  const bool charging,
						  const short devicebatteryLevel,
						  const short bikebatteryLevel);

	void makeStateUpdateSms(const char schema,
							const char type);
	
	void makeUiPosSms(const location_t *location);
};

#endif