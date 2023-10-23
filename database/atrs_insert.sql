USE atrs;

-- a
INSERT INTO airline (name) VALUES ('China Eastern');

-- b
INSERT INTO airport (name, city) 
VALUES ('JFK', 'NYC'),
	('PVG', 'Shanghai');

-- c
INSERT INTO customer (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth) 
VALUES ('customer1@example.com', 'Customer One', 'password1', '123', 'Street 1', 'City 1', 'State 1', '1234567890', 'P12345678', '2025-12-31', 'Country 1', '1990-01-01'),
       ('customer2@example.com', 'Customer Two', 'password2', '456', 'Street 2', 'City 2', 'State 2', '0987654321', 'P23456789', '2026-12-31', 'Country 2', '1991-01-01');

INSERT INTO booking_agent (email, password, booking_agent_id, airline_name) 
VALUES ('agentA@example.com', 'agentApassword', 'A12345', 'China Eastern');

-- d
INSERT INTO airplane (id, airline_name) 
VALUES ('Plane1', 'China Eastern'), 
       ('Plane2', 'China Eastern');

-- e
INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, permission, airline_name) 
VALUES ('staff1', 'password1', 'Staff', 'One', '1980-01-01', 'Full', 'China Eastern');

-- f
INSERT INTO flight (flight_num, airline_name, departure_time, arrival_time, price, status, airplane_id, arr_airport_name, dept_airport_name) 
VALUES (1, 'China Eastern', '2023-11-01 10:00:00', '2023-11-01 14:00:00', 200.00, 'Upcoming', 'Plane1', 'JFK', 'PVG'),
       (2, 'China Eastern', '2023-10-01 10:00:00', '2023-10-01 14:00:00', 250.00, 'InProgress', 'Plane2', 'PVG', 'JFK'),
       (3, 'China Eastern', '2023-09-01 10:00:00', '2023-09-01 14:00:00', 300.00, 'Delayed', 'Plane1', 'JFK', 'PVG');

-- g
INSERT INTO ticket (ticket_id, flight_num, airline_name, customer_email, booking_agent_email) 
VALUES ('T1', 1, 'China Eastern', 'customer1@example.com', NULL), 
       ('T2', 2, 'China Eastern', 'customer2@example.com', 'agentA@example.com');
