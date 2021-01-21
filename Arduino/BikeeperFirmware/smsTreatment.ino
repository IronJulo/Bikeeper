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
                sendSMSTo(userPhoneNumber, "Your are now sync with your device you can send command here type help for help");
                message("OK", 1000, 0);
                Serial.println("The user phone number is :"); // TODO delete
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
            String commandReceived = answer.substring(messageIndex, messageIndex + 4);
            Serial.print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*:");
            Serial.print("the index :");
            Serial.println(messageIndex);
            Serial.print("the word :");
            Serial.println(messageIndex);
            if (messageIndex >= 0)
            {
                if (messageIndex == 74)
                {
                    if (!parked)
                    {
                        if (journey)
                        {
                            sendSMSTo(userPhoneNumber, "You where doing a journey we stopped it for you and your bike is now parked");
                            message("OK", 1000, 0);
                            parked = true;
                            journey = false;
                        }
                        else
                        {
                            sendSMSTo(userPhoneNumber, "Your bike is now parked");
                            message("OK", 1000, 0);
                            parked = true;
                        }
                    }
                    else
                    {
                        sendSMSTo(userPhoneNumber, "Your Bike is already parked");
                        message("OK", 1000, 0);
                    }
                }
                messageIndex = answer.indexOf("unpark"); // Get the index if exist of the string "park"
                if (messageIndex == 74)
                {
                    if (parked)
                    {
                        sendSMSTo(userPhoneNumber, "Your Bike is now parked");
                        message("OK", 1000, 0);
                        parked = false;
                    }
                    else
                    {
                        sendSMSTo(userPhoneNumber, "Your Bike is not parked");
                        message("OK", 1000, 0);
                        parked = true;
                    }
                }

                messageIndex = answer.indexOf("start"); // Get the index if exist of the string "start"
                if (messageIndex == 74)
                {
                    if (journey)
                    {
                        sendSMSTo(userPhoneNumber, "You are already doing a journey please 'stop' it before starting a new one");
                        message("OK", 1000, 0);
                    }
                    else
                    {
                        if (parked)
                        {
                            sendSMSTo(userPhoneNumber, "You have started your journey and your bike is no unparked ride safe");
                            message("OK", 1000, 0);
                            journey = true;
                            parked = false;
                        }
                        else
                        {
                            sendSMSTo(userPhoneNumber, "You have started your journey ride safe");
                            message("OK", 1000, 0);
                            journey = true;
                        }
                    }
                }

                messageIndex = answer.indexOf("stop"); // Get the index if exist of the string "start"
                if (messageIndex == 74)
                {
                    if (journey)
                    {
                        sendSMSTo(userPhoneNumber, "You have stopped your journey remember to 'park' your bike for optimal detection");
                        message("OK", 1000, 0);
                        journey = false;
                    }
                    else
                    {
                        sendSMSTo(userPhoneNumber, "You are not doing a journey right now but you can 'start' one");
                        message("OK", 1000, 0);
                    }
                }
            }
        }
    }
}