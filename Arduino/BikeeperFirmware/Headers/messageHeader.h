#ifndef MESSAGES_HEADER_H
# define MESSAGES_HEADER_H

/**
 * @file messageHeader.h
 */

/** @struct message header
 * This struct is the Header of the message (SMS)
 * 
 * @var magic_t::magic
 *      the 4 first character mostly "[bk]"
 * 
 * @var magic_t::_separator0
 *      the first separator ";"
 * 
 * @var magic_t::schema
 *      the magic schema (to decode afterward in python)
 * 
 */     

struct header_t
{
	char magic[4];
	char _separator0;
	char schema;
	header_t(char schema):
		magic(),
		_separator0(';'),
		schema(schema)
		{
			memcpy(magic, "[bk]", 4);
		};

};

#endif