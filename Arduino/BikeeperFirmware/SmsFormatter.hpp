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
	void storeBikeAngle(const int angle);
	void setSeparator();

	void store(const char *arr);

	char *getStorage();

	void makeJourneySms(const char schema,
						const location_t *location,
						const bool charging,
						const double devicebatteryLevel,
						const double bikebatteryLevel,
						const short speed,
						const double angle);

	void makeAlertSms(const char schema,
					  const char type,
					  const location_t *location,
					  const bool charging,
					  const double devicebatteryLevel,
					  const double bikebatteryLevel);

	void makeHeartbeatSms(const char schema,
						  const location_t *location,
						  const bool charging,
						  const double devicebatteryLevel,
						  const double bikebatteryLevel);

	void makeStateUpdateSms(const char schema,
							const char type);
	
	void storebatt(const short bikebatteryLevel);
};

#endif