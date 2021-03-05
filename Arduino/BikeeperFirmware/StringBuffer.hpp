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
        void storeInt(int i);
        void storeInt3(int i);
        void storeSignedShort(short i);
        void storeShort(short i);
        void store(const char *arr);
        void storeDouble(double val, short len, short prec);
        void storeUnsignedDouble(double val, short len, short prec);

        void replaceTo(short index, char c);
        void toLower();

        void rewind();
        void skipTo(short index);

        short indexOf(const char *c);
        short indexOf(const char *c, short len);
        void substring(char *in, short from, short to);
        void tail(char *in);

        short length();

        void clear();

        char* getStorage();
};

#endif
