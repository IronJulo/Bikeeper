void
initCard(){
    Serial.println("Initialisation...");

    sim800l.println("AT");                                      // Start to talk to the SIM800L
    message("OK", 2000, 0);
    sim800l.println("AT+CMGD=1,4");
    message("OK", 2000, 0);
    while (userPhoneNumber == ""){
        if (message("+CMTI:", 1000, 1))
        {
            LireSMS();                                                  // Si nouveau SMS disponible SIM800 envoie +CMTI:
        }
    }
    sim800l.println("AT+CMGD=1,1");
    message("OK", 2000, 0);
}