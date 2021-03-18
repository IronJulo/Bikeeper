#include <Arduino.h>
#include <string.h>
#include <avr/pgmspace.h>

#include "Utils.hpp"
#include "StringBuffer.hpp"
#include "StringsSms.hpp"

bool arraysCompare(const char *left, const char *right)
{
	Serial.println(left);
	Serial.println(right);
	for (int i = 0 ; i < 11; i++)
	{
		if (left[i] != right[i]){
			return false;
		}
	}
	return true;
}

