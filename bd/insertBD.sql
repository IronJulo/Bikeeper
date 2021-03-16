-- Inserting a new user
INSERT INTO USER(username_user, password_user, num_user, firstname_user, lastname_user, email_user, town_user, postal_code_user, street_user, is_admin_user)
VALUES("PhoqueEberlue", "1234", "+33615498730", "Andrew", "Mary Huet de Barochez", "phoqueeberlue@gmail.com", "Chartres", "45100", "79 Rue de Georges lafont", 0);
-- Inserting a new device
INSERT INTO DEVICE(num_device, name_device, row_parameters_device, username_user)
VALUES("0631704631", "julesBiKeeper", "", "user1");
-- Inserting a new log
INSERT INTO LOG(content_log, type_log, datetime_log, exception_log, num_device)
VALUES("content", "init", NOW(), "None", "+33625927620");
-- Inserting a new contact
INSERT INTO CONTACT(num_contact, firstname_contact, lastname_contact, profile_picture_contact, num_device)
VALUES("0677168763", "Kevin", "Talland", "", "0631704631");
INSERT INTO CONTACT(num_contact, firstname_contact, lastname_contact, profile_picture_contact, num_device)
VALUES("0778151422", "Fabien", "Billaut", "", "0631704631");
-- Inserting a new ticket
INSERT INTO TICKET(is_closed_ticket, username_user)
VALUES(0, "PhoqueEberlue");
-- Insert a new message
INSERT INTO MESSAGE(is_admin_message, datetime_message, title_message, content_message, id_ticket)
VALUES(0, NOW(), "MON BIKEEPER NE FONCTIONNE PLUS CEST QUOI CETTE MERDE", "Bonjour mon bikeeper ne fonctionne plus, c'est très facheux nonobstant", 1);
INSERT INTO MESSAGE(is_admin_message, datetime_message, title_message, content_message, id_ticket)
VALUES(1, NOW(), "RE: MON BIKEEPER NE FONCTIONNE PLUS CEST QUOI CETTE MERDE", "Bonjour pourriez spécifiez d'avantage vos problèmes ? Cordialement MHDB.", 1);
-- Select all devices of a given user
SELECT num_device, row_parameters_device
FROM DEVICE
WHERE username_user = "PhoqueEberlue";
-- Select every emergency contacts from a device
SELECT id_contact, num_contact, firstname_contact, lastname_contact
FROM CONTACT
WHERE num_device = "+33625927620";
-- Select all logs from a given device
SELECT id_log, content_log, type_log, datetime_log, exception_log
FROM LOG
WHERE num_device = "+33625927620";