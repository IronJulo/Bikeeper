
class SoftwareSerial;
class StringBuffer;

class I_Sim800L
{
    private :
        StringBuffer *m_stringBuffer;
        SoftwareSerial *m_softwareSerial;

    public :
        I_Sim800L(SoftwareSerial *serial, StringBuffer *stringBuffer);

        void begin(unsigned int baudrate);
        void listen();
        void send(const char *to, const char *msg);
        void init(char userPhoneNumber[], const char serverPhoneNumber[]);
        void readii(unsigned int timeout);
        void deleteAllSms();
        bool smartRead(const char waiting[], short waitingSize, unsigned int timeout);
        void initTreatement(char userPhoneNumber[], const char serverPhoneNumber[]);
    private:
        template <typename T>
          void sendCommand(T cmd)
          {
            m_softwareSerial->print(cmd);
          }
};
