USE atrs;

-- Adding airlines for diversity in flight options
INSERT INTO airline (name) 
VALUES ('China Eastern'),
       ('American Airlines'),
       ('Delta Air Lines');

-- Adding airports to cover different cities
INSERT INTO airport (name, city) 
VALUES ('JFK', 'New York'),
       ('PVG', 'Shanghai'),
       ('LAX', 'Los Angeles'),
       ('HND', 'Tokyo'),
       ('LHR', 'London');

-- Adding customers with diverse destinations and origins
INSERT INTO customer (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth) 
VALUES ('customer1@example.com', 'Oliver One', 'password1', '123', 'Street 1', 'City 1', 'State 1', '1234567890', 'P12345678', '2025-12-31', 'Country 1', '1990-01-01'),
       ('customer2@example.com', 'Thomas Two', 'password2', '456', 'Street 2', 'City 2', 'State 2', '9876543210', 'P23456789', '2026-12-31', 'Country 2', '1991-01-01'),
       ('customer3@example.com', 'Tim Three', 'password3', '789', 'Street 3', 'City 3', 'State 3', '1111111111', 'P34567890', '2027-12-31', 'Country 3', '1992-01-01'),
       ('customer4@example.com', 'Freddie Four', 'password4', '101', 'Street 4', 'City 4', 'State 4', '2222222222', 'P45678901', '2028-12-31', 'Country 4', '1993-01-01');

-- Adding booking agents working for different airlines
INSERT INTO booking_agent (email, password, airline_name) 
VALUES ('agentA@example.com', 'agentApassword', 'Delta Air Lines'),
       ('agentB@example.com', 'agentBpassword', 'American Airlines'),
       ('agentC@example.com', 'agentCpassword', 'Delta Air Lines');

-- Adding booking agents working for different airlines
INSERT INTO booking_agent_workfor (booking_agent_id, airline_name)
VALUES (1, 'Delta Air Lines'),
       (1, 'American Airlines'),
       (2, 'American Airlines'),
       (2, 'China Eastern'),
       (3, 'Delta Air Lines');

-- Adding airplanes to the system
INSERT INTO airplane (airline_name, seat_num) 
VALUES ('China Eastern', 100),
       ('American Airlines', 200),
       ('Delta Air Lines', 300);

-- Adding airline staff with different permissions and airlines
-- "Admin" permission staff can create flights, add airplanes/airports, grant permissions
-- "Operator" permission staff can change flight status
-- NULL permission staff can only view flights
INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, permission, airline_name) 
VALUES ('adminStaff', 'adminPass', 'Alice', 'Admin', '1975-01-01', 'Admin', 'American Airlines'),
       ('operatorStaff', 'operatorPass', 'Oscar', 'Operator', '1985-01-01', 'Operator', 'Delta Air Lines'),
       ('normalStaff', 'normalPass', 'Nick', 'Normal', '1995-01-01', NULL, 'American Airlines');

-- Adding more flights covering various statuses and airlines
INSERT INTO flight (airline_name, departure_time, arrival_time, price, status, airplane_id, arr_airport_name, dept_airport_name) 
VALUES ('China Eastern', '2023-11-01 10:00:00', '2023-11-01 14:00:00', 200.00, 'Upcoming', 1, 'JFK', 'PVG'),
       ('China Eastern', '2023-10-01 10:00:00', '2023-10-01 14:00:00', 250.00, 'InProgress', 1, 'PVG', 'JFK'),
       ('China Eastern', '2023-09-01 10:00:00', '2023-09-01 14:00:00', 300.00, 'Delayed', 1, 'JFK', 'PVG'),
       ('American Airlines', '2023-12-01 10:00:00', '2023-12-01 15:00:00', 350.00, 'Upcoming', 2, 'LAX', 'HND'),
       ('Delta Air Lines', '2023-12-02 11:00:00', '2023-12-02 16:00:00', 400.00, 'Delayed', 3, 'LHR', 'LAX');

-- Adding tickets for new flights and customers
INSERT INTO ticket (flight_num, airline_name, customer_email, purchase_date)
VALUES (1, 'China Eastern', 'customer3@example.com', '2023-9-30 10:00:00'),
       (1, 'China Eastern', 'customer2@example.com', '2023-9-25 10:00:00'),
       (2, 'China Eastern', 'customer2@example.com', '2023-8-30 10:00:00'),
       (3, 'China Eastern', 'customer1@example.com', '2023-7-30 10:00:00'),
       (4, 'American Airlines', 'customer1@example.com', '2023-11-30 10:00:00'),
       (5, 'Delta Air Lines', 'customer4@example.com', '2023-12-01 10:00:00'),
       (5, 'Delta Air Lines', 'customer3@example.com', '2023-12-01 10:00:00');
