void treatSMS(String answer)
{

    if (userPhoneNumber == "") // Check if the phone number is not defined
    {
        if (senderPhoneNumber == SERVER_PHONE_NUMBER) // Check who is sending us SMS (if it's the SERVER)
        {

            int userPhonenumberIndex = answer.indexOf("+33");
            if (userPhonenumberIndex >= 0)
            {
                userPhoneNumber = answer.substring(userPhonenumberIndex, userPhonenumberIndex + 12);
                sendSMSTo(userPhoneNumber, StringSyncOk);
                message("OK", 1000, 0);
                Serial.println(F("The user phone number is :")); // TODO delete
                Serial.println(userPhoneNumber);              // TODO delete
            }
        }
    }
    else
    {
        if (senderPhoneNumber == SERVER_PHONE_NUMBER || senderPhoneNumber == userPhoneNumber)
        {
            answer.toLowerCase();
            int messageIndex = answer.indexOf("park");
            String commandReceived = answer.substring(74, answer.length() - 5);                           //74 is the lenght of the data before the actual sms
            commandReceived.trim();
            //commandReceived.replace(String(char(10)), "");
            //commandReceived.replace(String(char(13)), "");
            Serial.println(F("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"));
            Serial.println(commandReceived == "park");
            Serial.println(commandReceived.length());
            Serial.println(commandReceived);

            if (commandReceived != "")
            {
                if (commandReceived == "unpark")
                {
                    if (parked)
                    {
                        sendSMSTo(userPhoneNumber, StringBikeUnparked);
                        message("OK", 1000, 0);
                        parked = false;
                    }
                    else
                    {
                        sendSMSTo(userPhoneNumber, StringBikeNotParked);
                        message("OK", 1000, 0);
                        parked = true;
                    }
                }

                if (commandReceived == "park")
                {
                    if (!parked)
                    {
                        if (journey)
                        {
                            sendSMSTo(userPhoneNumber, StringJourneyStopedAndParked);
                            message("OK", 1000, 0);
                            parked = true;
                            journey = false;
                        }
                        else
                        {
                            sendSMSTo(userPhoneNumber, StringBikeParked);
                            message("OK", 1000, 0);
                            parked = true;
                        }
                    }
                    else
                    {
                        sendSMSTo(userPhoneNumber, StringBikeAlreadyParked);
                        message("OK", 1000, 0);
                    }
                }
                if (commandReceived == "start")
                {
                    if (journey)
                    {
                        sendSMSTo(userPhoneNumber, StringJourneyStartedPleaseStop);
                        message("OK", 1000, 0);
                    }
                    else
                    {
                        if (parked)
                        {
                            sendSMSTo(userPhoneNumber, StringJourneyStartedAndUnparked);
                            message("OK", 1000, 0);
                            journey = true;
                            parked = false;
                        }
                        else
                        {
                            sendSMSTo(userPhoneNumber, StringJourneyStarted);
                            message("OK", 1000, 0);
                            journey = true;
                        }
                    }
                }

                if (commandReceived == "stop")
                {
                    if (journey)
                    {
                        sendSMSTo(userPhoneNumber, StringJourneyStopped);
                        message("OK", 1000, 0);
                        journey = false;
                    }
                    else
                    {
                        sendSMSTo(userPhoneNumber, StringJourneyNotStarted);
                        message("OK", 1000, 0);
                    }
                }
            }
        }
    }
}