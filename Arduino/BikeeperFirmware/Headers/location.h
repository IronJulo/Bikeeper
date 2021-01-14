#ifndef LOCATION_H
#define LOCATION_H

struct location_t
{
	double latitude;
	double longitude;

	location_t() : 
		latitude(),
		longitude()
	{
	};
};

#endif