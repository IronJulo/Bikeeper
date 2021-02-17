/**
 * Function that store an int in 3 characetr long array
 * 
 */
void
storeInt3(int value, char *into)
{
	char buff[4] = { '0' };
	itoa(value, buff + (value < 100) + (value < 10), 10);
	memcpy(into, buff, 3);
}



/**
 * Function that store an signed doube in an char array (if >0 - else +)
 * 
 */
void
storeSignedDouble(double value, int width, int precision, char *into)
{
	char buff[40] = { '0' };
	buff[0] = value < 0 ? '-' : '+';
	dtostrf(fabs(value), width, precision, buff + 1);
	memcpy(into, buff, width + 1);
}

/**
 * Function that store an int in 4 characetr long array
 * 
 */
void
storeInt4(int value, char *into)
{
	char buff[5] = { '0' };
	itoa(value, buff + (value < 1000) + (value < 100) + (value < 10), 10);
	memcpy(into, buff, 4);
}

/**
 * Function that store an int in 4 characetr long array
 * 
 */
void
storeSignedInt4(int value, char *into)
{
	char buff[5] = { '0' };
    buff[0] = value < 0 ? '-' : '+';
	itoa(value, buff + (value < 100) + (value < 10), 10);
	memcpy(into, buff, 4);
}