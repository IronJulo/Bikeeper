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
        void toLower();

        void rewind();

        short indexOf(const char *c);
        short indexOf(const char *c, short len);
        void substring(char *in, short from, short to);
        void tail(char *in);

        short length();

        void clear();

        char* getStorage();
};

#endif
