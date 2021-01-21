int led = 13;
String answer, senderPhoneNumber, SMS;
String userPhoneNumber;
unsigned long t0;
#define GSM_RX 7       // Declare the SIM800L onto the pin 7.
#define GSM_TX 8       // Declare the SIM800L onto the pin 8.
#define STR_LENGTH 160 // SMS lenght max 160 (one sms in limited in size !).
#include <SoftwareSerial.h>
#define SERVER_PHONE_NUMBER "+33769342048"
SoftwareSerial sim800l(GSM_RX, GSM_TX);

void setup()
{
    sim800l.begin(9600);
    Serial.begin(9600);
    delay(2000);
    Serial.println("Initialisation...");
    sim800l.println("AT");
    while (!message("OK", 1000, 0))
        sim800l.println("AT");
    sim800l.println("AT+CNUM"); // Affiche n° de la carte SIM utilisée
    message("OK", 20000, 1);
    Serial.print("Qualite reseau : ");
    sim800l.println("AT+CSQ"); // Qualité du réseau, pb si CSQ = 0
    message("OK", 10000, 1);
    sim800l.println("AT+CMGF=1"); // Mode Texte
    message("OK", 1000, 0);
    sim800l.println("AT+CMGD=1,4"); // effacer les SMS en mémoire dans la carte SIM
    sim800l.println("AT+CMGD=?");
    message("OK", 2000, 0);         // car on lit toujours le message N°1 de la carte SIM...
}

void loop()
{
    if (message("+CMTI:", 1000, 1))
    {
        LireSMS(); // Si nouveau SMS disponible SIM800 envoie +CMTI:
    }
        Serial.println("le nouveau numero de tel est");
        Serial.println(senderPhoneNumber);
}

void LireSMS()
{
    sim800l.println("AT+CMGF=1"); // Mode Texte
    message("OK",1000,0);
    sim800l.println("AT+CMGR=1"); // Only read the first sms on the sim card!
    message("OK",1000,0);

    int phoneIndex = answer.indexOf("+33"); // get sender phone number index
     Serial.println("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
    Serial.println(answer);
    Serial.println("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
    senderPhoneNumber = answer.substring(phoneIndex, phoneIndex + 12); // get sender phone number

    answer[phoneIndex] = 'a'; //delete the old + from the sender phone number

    Serial.println("SMS recu depuis : " + senderPhoneNumber);
    if (senderPhoneNumber == SERVER_PHONE_NUMBER)
    {
        int userPhoneIndex = answer.indexOf("+33"); //It's the server talking to us
        if (userPhoneIndex >= 0)
        {
            userPhoneNumber = answer.substring(userPhoneIndex, userPhoneIndex + 12);
            Serial.println("le nouveau numero de tel est");
            Serial.println(userPhoneNumber);
        }
        Serial.println("le nouveau numero de tel est");
        Serial.println(senderPhoneNumber);
    }
    if (answer.indexOf("led on") >= 0)
    {
        Serial.println("on est la on est chez nousd");
        SMS = "Ordre recu : Allumer LED !";
        digitalWrite(led, 1);
    }
    else
    {
        if (answer.indexOf("led off") >= 0)
        {
            SMS = "Ordre recu : Eteindre LED !";
            digitalWrite(led, 0);
        }
        else
            SMS = "Ordre non compris !";
    }
    Serial.println("le nouveau numero de tel est");
    Serial.println(userPhoneNumber);
    sim800l.println("AT+CMGD=1,4"); // effacer les SMS de la Carte SIM
    message("OK", 1000, 0);
    Serial.println(SMS);
    Serial.println("");

    // Envoyer la confirmation de l'ordre par SMS
    Serial.println("Envoi message confirmation");
    sim800l.println("AT+CMGS=\"" + senderPhoneNumber + "\"");
    message(">", 1000, 0);
    sim800l.println(SMS);
    sim800l.write(26); // Caractère de fin 26 <Ctrl-Z>
    sim800l.println("");
    message("+CMGS:", 10000, 1);
}

boolean message(String attente, unsigned int timeout, boolean affiche)
{
    t0 = millis();
    answer = "";
    while (millis() - t0 < timeout)
    {
        while (sim800l.available())
            answer.concat(char(sim800l.read()));
        if (answer.indexOf(attente) >= 0)
        {               // Lit encore 100 ms le port série
            delay(100); // pour être sur de ne rien louper...
            while (sim800l.available())
                answer.concat(char(sim800l.read()));
            break;
        }
    }
    if (affiche || answer.indexOf(attente) == -1)
    {
        Serial.print("Attente = " + attente + " " + answer.indexOf(attente) + " duree ");
        Serial.print(millis() - t0);
        Serial.println(" ms");
        Serial.println(answer);
    }

    if (answer.indexOf(attente) > 0)
        return true;
    else
        return false;
}
