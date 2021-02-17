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

void StringBuffer::store(int i)
{
	if (m_index < m_length)
	{
		m_storage[m_index++] = i;
	}
}

void StringBuffer::rewind()
{
	m_index = 0;
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
