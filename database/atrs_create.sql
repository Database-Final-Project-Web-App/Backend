/* 
Convention of datatype
- name: VARCHAR(100)
- id: VARCHAR(10)
- password: VARCHAR(100)
- email VARCHAR(100)

*/

USE atrs;

CREATE TABLE airline(
    name VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY(name)
);

CREATE TABLE airline_staff(
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    permission VARCHAR(10),
    airline_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(username),
    FOREIGN KEY(airline_name) REFERENCES airline(name)
);

CREATE TABLE airplane(
    airplane_id INT AUTO_INCREMENT,
    airline_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(airplane_id),
    FOREIGN KEY(airline_name) REFERENCES airline(name)
);

CREATE TABLE airport(
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    PRIMARY KEY(name)
);

CREATE TABLE booking_agent(
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    booking_agent_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    airline_name VARCHAR(100),
    PRIMARY KEY(email),
    FOREIGN KEY(airline_name) REFERENCES airline(name)
);

CREATE TABLE flight(
    flight_num INT AUTO_INCREMENT NOT NULL,
    airline_name VARCHAR(100) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    price NUMERIC(15, 5) NOT NULL,
    status VARCHAR(10) NOT NULL,
    airplane_id INT NOT NULL,
    arr_airport_name VARCHAR(100) NOT NULL,
    dept_airport_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(flight_num, airline_name),
    FOREIGN KEY(airplane_id) REFERENCES airplane(airplane_id),
    FOREIGN KEY(airline_name) REFERENCES airline(name),
    /* FOREIGN KEY(airplane_id, airline_name) REFERENCES airplane(airplane_id, airline_name), */
    FOREIGN KEY(arr_airport_name) REFERENCES airport(name),
    FOREIGN KEY(dept_airport_name) REFERENCES airport(name)
);

CREATE TABLE customer(
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    building_number VARCHAR(100),
    street VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    phone_number VARCHAR(20) NOT NULL,
    passport_number VARCHAR(100) NOT NULL UNIQUE,
    passport_expiration DATE NOT NULL,
    passport_country VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    PRIMARY KEY(email)
);

CREATE TABLE ticket(
    ticket_id INT AUTO_INCREMENT,
    flight_num INT NOT NULL,
    airline_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100) NOT NULL,
    booking_agent_email VARCHAR(100),
    purchase_date DATETIME NOT NULL,
    PRIMARY KEY(ticket_id),
    FOREIGN KEY(flight_num) REFERENCES flight(flight_num),
    FOREIGN KEY(airline_name) REFERENCES flight(airline_name),
    /* FOREIGN KEY(flight_num, airline_name) REFERENCES flight(flight_num, airline_name), */

    FOREIGN KEY(customer_email) REFERENCES customer(email),
    FOREIGN KEY(booking_agent_email) REFERENCES booking_agent(email)
);
