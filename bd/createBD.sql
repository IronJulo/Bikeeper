CREATE DATABASE IF NOT EXISTS BIKEEPER DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE BIKEEPER;

DROP TABLE CONTACT;
DROP TABLE MESSAGE;
DROP TABLE TICKET;
DROP TABLE LOG;
DROP TABLE DEVICE;
DROP TABLE USER;

CREATE TABLE CONTACT (
  id_contact INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  num_contact VARCHAR(15),
  firstname_contact VARCHAR(42),
  lastname_contact VARCHAR(42),
  profile_picture_contact VARCHAR(100),
  num_device VARCHAR(15)
);

CREATE TABLE LOG (
  id_log INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  content_log VARCHAR(160),
  type_log VARCHAR(20),
  datetime_log DATETIME,
  exception_log VARCHAR(160),
  num_device  VARCHAR(15)
);

CREATE TABLE DEVICE (
  num_device VARCHAR(15),
  name_device VARCHAR(42),
  row_parameters_device VARCHAR(200),
  username_user VARCHAR(42),
  PRIMARY KEY (num_device)
);

CREATE TABLE USER (
  username_user VARCHAR(42),
  password_user VARCHAR(200),
  num_user VARCHAR(15),
  firstname_user VARCHAR(42),
  lastname_user VARCHAR(42),
  email_user VARCHAR(80),
  town_user VARCHAR(42),
  postal_code_user INT(10),
  street_user VARCHAR(95),
  profile_picture_user VARCHAR(100),
  is_admin_user TINYINT,
  PRIMARY KEY (username_user)
);

CREATE TABLE MESSAGE (
  id_message INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  is_admin_message TINYINT,
  datetime_message DATETIME,
  content_message VARCHAR(1000),
  id_ticket INT
);

CREATE TABLE TICKET (
  id_ticket INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  title_ticket VARCHAR(100),
  is_closed_ticket TINYINT,
  username_user VARCHAR(42)
);

ALTER TABLE CONTACT ADD FOREIGN KEY (num_device) REFERENCES DEVICE (num_device);
ALTER TABLE DEVICE ADD FOREIGN KEY (username_user) REFERENCES USER (username_user);
ALTER TABLE MESSAGE ADD FOREIGN KEY (id_ticket) REFERENCES TICKET (id_ticket);
ALTER TABLE TICKET ADD FOREIGN KEY (username_user) REFERENCES USER (username_user);
ALTER TABLE LOG ADD FOREIGN KEY (num_device) REFERENCES DEVICE (num_device);