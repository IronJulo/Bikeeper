#ifndef LOCATION_H
#define LOCATION_H

struct location_t
{
	float latitude;
	float longitude;

	location_t() : 
		latitude(),
		longitude()
	{
	};
};

#endif