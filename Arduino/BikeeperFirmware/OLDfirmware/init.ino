void
initCard(){
    sim800l.listen();
    Serial.println("Initialisation...");

    sim800l.println("AT");                                      // Start to talk to the SIM800L
    message("OK", 1000, 0);

    sim800l.println("AT+CMGDA=DEL INBOX");
    message("OK", 1000, 0);

    sim800l.println("AT+CMGD=1,2");
    message("OK", 2000, 0);
    sim800l.println("\r");
    sim800l.println("AT+CMGD=1,2");
    sim800l.println("\r");
    while (userPhoneNumber == ""){
        if (message("+CMTI:", 1000, 1))
        {
            LireSMS();                                                  // Si nouveau SMS disponible SIM800 envoie +CMTI:
            sim800l.println("AT+CMGD=1,2");

            Serial.print(F("answer : "));
            Serial.println(answer);
            Serial.println();

            message("OK", 1000, 0); 


        }

        Serial.println(F("waiting for an sms"));
        Serial.print(F("user phone number : "));
        Serial.println(userPhoneNumber);
    }
    //sim800l.println("AT+CMGDA=1");
    sim800l.println("\r");
    sim800l.println("\r");
    sim800l.println("\r");
    sim800l.println("AT+CMGDA=DEL ALL");
    
    message("+CMGS", 30000, 0); 
}