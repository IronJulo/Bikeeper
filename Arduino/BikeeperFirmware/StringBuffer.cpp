#include <Arduino.h>
#include <string.h>
#include <math.h>
#include <SoftwareSerial.h>

#include "StringBuffer.hpp"
#include "Utils.hpp"

StringBuffer::StringBuffer(char *storage, short length) : m_storage(storage), m_length(length), m_index(0)
{
	clear();
};

void StringBuffer::store(char c)
{
	if (m_index < m_length)
	{
		m_storage[m_index++] = c;
	}
}

/*void StringBuffer::storeInt(int i)
{
	if (m_index < m_length)
	{
		char buff[4] = { '0' };
		itoa(value, buff + (value < 100) + (value < 10), 10);
		memcpy(into, buff, 3);
	}
}*/


void StringBuffer::storeInt3(int i)
{
	if (m_index < m_length)
	{
		char buff[4] = { '0' };
		itoa( i, buff + ( i < 100) + ( i < 10), 10);
		memcpy(m_storage + m_index, buff, 3);
		m_index += 3;
	}
}

void StringBuffer::storeSignedShort(short i)
{
	if (m_index < m_length)
	{
		char buff[5] = { '0' };
		buff[0] = i < 0 ? '-' : '+';
		itoa( i, buff + ( i < 100) + ( i < 10), 10);
		memcpy(m_storage + m_index, buff, 3);
		m_index += 4;
	}
}

/* TODO */
void StringBuffer::storeShort(short i)
{
	if (m_index < m_length)
	{
		while (i)
		{
			m_storage[m_index++] = i % 10 + '0';
			i /= 10;
		}
	}
}

void StringBuffer::storeDouble(double val, short len, short prec)
{
	m_index > 0 ? m_index-- : m_index;

	store(val < 0 ? '-' : '+');
	dtostrf(fabs(val), len, prec, m_storage + m_index);
	m_index = m_index + len;
}

void StringBuffer::storeUnsignedDouble(double val, short len, short prec)
{
	m_index > 0 ? m_index-- : m_index;

	dtostrf(fabs(val), len, prec, m_storage + m_index);
	m_index = m_index + len;
}

void StringBuffer::store(const char *arr)
{
	m_index > 0 ? m_index-- : m_index;
	for (short i = 0; i < strlen(arr); i++)
	{
		store(arr[i]);
	}
}

void StringBuffer::rewind()
{
	m_index = 0;
}

void StringBuffer::skipTo(short index)
{
	m_index = index;
}

short StringBuffer::indexOf(const char *c, short len)
{
	bool found = false;
	for (short i = 0; i < m_length; i++)
	{
		if (m_storage[i] == c[0])
		{
			found = true;
			if (i + len <= m_length)
			{
				for (int j = 0; j < len; j++)
				{
					if (found && m_storage[i + j] != c[j])
					{
						found = false;
						break;
					}
				}
			}
			if (found)
			{
				return (i);
			}
		}
	}

	return (-1);
}

short StringBuffer::indexOf(const char *c)
{
	for (short i = 0; i < m_length; i++)
	{
		if (m_storage[i] == &c)
		{
			return (i);
		}
	}
	return (-1);
}

void StringBuffer::substring(char *in, short from, short to)
{
	if (from >= 0 /* && to <= m_index*/)
	{
		for (int i = from; i < to; i++)
		{
			in[i - from] = m_storage[i];
		}
	}
	in[to - from] = '0';
}

short StringBuffer::length()
{
	return (m_length);
}

void StringBuffer::clear()
{
	memset(m_storage, 0, m_length);
	m_index = 0;
}

char *
StringBuffer::getStorage()
{
	return m_storage;
}

void StringBuffer::replaceTo(short index, char c)
{
	m_storage[index] = c;
}

void StringBuffer::toLower()
{
	for (short i = 0; i < m_index; i++)
	{
		m_storage[i] = tolower(m_storage[i]);
	}
}
