CREATE DATABASE nsec;

USE nsec;

CREATE TABLE leads (
  lead_id VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL,
  street VARCHAR(255),
  city VARCHAR(255),
  state VARCHAR(255),
  postalcode VARCHAR(255),
  status ENUM ('SCHEDULED', 'FOLLOWUP', 'CLOSED') NOT NULL,
  associate_canvasser_email VARCHAR(255),
  associate_salesrep_email VARCHAR(255)
);

CREATE TABLE associates (
  associate_id VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  phone_number VARCHAR(255),
  email VARCHAR(255) UNIQUE NOT NULL,
  role ENUM ('SALES', 'CANVASSER', 'USER', 'ADMIN') NOT NULL DEFAULT "USER"
);

CREATE TABLE people (
  person_id VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL,
  lead_id VARCHAR(255),
  main BOOLEAN NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  email VARCHAR(255),
  phone_number VARCHAR(255)
);

CREATE TABLE notes (
  note_id VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL,
  lead_id VARCHAR(255),
  content text NOT NULL,
  created_at DATETIME
);

CREATE TABLE appointments (
  appointment_id VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL,
  lead_id VARCHAR(255),
  start_time DATETIME,
  end_time DATETIME
);

CREATE TABLE files (
  file_id VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL,
  lead_id VARCHAR(255),
  aws_location VARCHAR(255),
  dbx_location VARCHAR(255),
  name VARCHAR(255)
);

ALTER TABLE leads ADD FOREIGN KEY (associate_canvasser_email) REFERENCES associates (email);

ALTER TABLE leads ADD FOREIGN KEY (associate_salesrep_email) REFERENCES associates (email);

ALTER TABLE people ADD FOREIGN KEY (lead_id) REFERENCES leads (lead_id);

ALTER TABLE notes ADD FOREIGN KEY (lead_id) REFERENCES leads (lead_id);

ALTER TABLE appointments ADD FOREIGN KEY (lead_id) REFERENCES leads (lead_id);

ALTER TABLE files ADD FOREIGN KEY (lead_id) REFERENCES leads (lead_id);
