void 
sendSMSTo(char* sms)
{
    Serial.println("Sending SMS...");                      //TODO delete
    sim800l.print("AT+CMGF=1\r");                          //Set the module to SMS mode
    delay(1000);
    sim800l.print("AT+CMGS=\"" PHONE_NUMBER "\"\r");           //Phone number /!\ include your country code, example +212123456789"
    delay(1000);
    sim800l.print(sms);          
    sim800l.print((char)26);                               // End of line char!
    sim800l.println();                                     //TODO delete
    Serial.println("Text Sent.");                          //TODO delete 
}
