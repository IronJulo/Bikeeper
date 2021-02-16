#ifndef STRINGBUFFER_H
#define STRINGBUFFER_H

class StringBuffer
{
    private :
        char *m_storage;
        short m_length;
        short m_index;

    public:
        StringBuffer(char *storage, short length);

        void store(char c);
        void store(int i);
        void store(double d);

        void replaceTo(short index, char c);

        void rewind();
        void skip(short n);

        short indexOf(char c);
        short indexOf(char *c, short len);
        void substring(char *in, short from, short to);

        short length();

        void clear();

        char* getStorage();
};

#endif
