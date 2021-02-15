
class SoftwareSerial;
class StringBuffer;

class I_Sim800L
{
    private :
        StringBuffer *m_stringBuffer;
        SoftwareSerial *m_softwareSerial;

    public :
        I_Sim800L(SoftwareSerial *serial, StringBuffer *stringBuffer);

        void send(const char *to, const char *msg);
        void init();
        void readii(unsigned int timeout);
        void deleteAllSms();
        bool smartRead(const char waiting, unsigned int timeout);
    private:
        template <typename T>
          void sendCommand(T cmd)
          {
            m_softwareSerial->print(cmd);
          }
};
