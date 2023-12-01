/* 
Convention of datatype
- name: VARCHAR(100)
- id: VARCHAR(10)
- password: VARCHAR(100)
- num: INT(20)
- email VARCHAR(100)

*/

#USE atrs;

CREATE TABLE airline(
	name	VARCHAR(100),
	PRIMARY KEY(name)
);

CREATE TABLE airline_staff(
	username		VARCHAR(100),
	password		VARCHAR(100) NOT NULL,
	first_name		VARCHAR(100),
	last_name		VARCHAR(100),
	date_of_birth	TIMESTAMP,
	permission		VARCHAR(10),
	airline_name	VARCHAR(100),
	PRIMARY KEY(username),
	FOREIGN KEY(airline_name) REFERENCES airline(name)
);

CREATE TABLE airplane(
	id				VARCHAR(10),
	airline_name 	VARCHAR(100),	
	PRIMARY KEY(id, airline_name),
	FOREIGN KEY(airline_name) REFERENCES airline(name)
);

CREATE TABLE airport(
	name	VARCHAR(100) NOT NULL,
	city	VARCHAR(100),
	PRIMARY KEY(name)
);

CREATE TABLE booking_agent(
	email				VARCHAR(100),
	password			VARCHAR(100) NOT NULL,
	booking_agent_id	VARCHAR(10) NOT NULL,
	airline_name		VARCHAR(100),
	PRIMARY KEY(email),
	FOREIGN KEY(airline_name) REFERENCES airline(name)
);

CREATE TABLE flight(
	flight_num			INT(20),
	airline_name		VARCHAR(100),
	departure_time		DATETIME,
	arrival_time		DATETIME,
	price				NUMERIC(15, 5),		
	status				VARCHAR(10),
	airplane_id			VARCHAR(10),
	arr_airport_name	VARCHAR(100),
	dept_airport_name	VARCHAR(100),
	PRIMARY KEY(flight_num, airline_name),
	FOREIGN KEY(airline_name) REFERENCES airline(name),
	FOREIGN KEY(arr_airport_name) REFERENCES airport(name),
	FOREIGN KEY(dept_airport_name) REFERENCES airport(name)
);

CREATE TABLE customer(
	email				VARCHAR(100),
	name				VARCHAR(100),
	password			VARCHAR(100),
	building_number		VARCHAR(100),
	street				VARCHAR(100),
	city				VARCHAR(100),
	state				VARCHAR(100),
	phone_number		VARCHAR(20),
	passport_number		VARCHAR(100),
	passport_expiration	VARCHAR(100),
	passport_country	VARCHAR(100),
	date_of_birth		TIMESTAMP,
	PRIMARY KEY(email)
);

CREATE TABLE ticket(
	ticket_id				VARCHAR(10),
	flight_num				INT(20),
	airline_name			VARCHAR(100),
	customer_email			VARCHAR(100),
	booking_agent_email		VARCHAR(100),
	purchase_date			DATETIME
	PRIMARY KEY(ticket_id),
	FOREIGN KEY(flight_num) REFERENCES flight(flight_num),
	FOREIGN KEY(airline_name) REFERENCES airline(name),
	FOREIGN KEY(customer_email) REFERENCES customer(email),
	FOREIGN KEY(booking_agent_email) REFERENCES booking_agent(email)
);



