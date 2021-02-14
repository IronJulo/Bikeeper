/**
 * Function that send a sms to the phone number passed in parameter
 * @param number String the number to witch we will send the sms
 * @param sms String the actual sms to send
 * 
 */

void sendSMSTo(String number, String sms) 
{
    noInterrupts();                                             // Stop interrupts
    Serial.println("Sending SMS...");                           // TODO delete
    sim800l.print("AT+CMGF=1\r");                               // Set the module to SMS mode
    delay(1000);                                                // Wait for Stability
    sim800l.print("AT+CMGS=\"");                                // Recipient phone number = next line
    sim800l.print(number);                                      // Send the number to the SIM800L
    sim800l.print("\"\r");                                      // Line break
    delay(1000);                                                // Wait for Stability
    sim800l.print(sms);                                         // Send the sms to the SIM800L
    sim800l.print((char)26);                                    // End of line char!
    sim800l.println();                                          // TODO delete
    Serial.println("Text Sent.");                               // TODO delete
    interrupts();                                               // Activate interrupts
}

void LireSMS()
{
    sim800l.println("AT+CMGF=1");                                         // Mode Texte TODO delete
    message("OK", 1000, 0);                                               // Wait for the SIM800L to return "OK" for stability
    sim800l.println("AT+CMGR=1");    
    sim800l.println("\r");                                      // Only read the first sms on the sim card!
    message("OK", 1000, 0);                                               // Wait for the SIM800L to return "OK" for stability

    int phoneIndex = answer.indexOf("+33");                               // Get sender phone number index (the first of the received text)
    senderPhoneNumber = answer.substring(phoneIndex, phoneIndex + 12);    // Get sender phone number 
    answer[phoneIndex] = 'a';                                             // Replace the first phone number "+" by a to get the next
    Serial.print("sender phone number : ");                               // TODO delete
    Serial.println(senderPhoneNumber);                                    // TODO delete

    treatSMS(answer);

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
