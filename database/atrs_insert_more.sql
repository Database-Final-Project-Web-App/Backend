USE atrs;

-- Adding airlines for diversity in flight options
INSERT INTO airline (name) 
VALUES  ('China Eastern'),
        ('American Airlines'),
        ('Delta Air Lines'),
        ('United Airlines'),
        ('Air Canada'),
        ('Air France'),
        ('Air India'),
        ('Air New Zealand'),
        ('Alaska Airlines'),
        ('All Nippon Airways'),
        ('British Airways'),
        ('Cathay Pacific'),
        ('Emirates'),
        ('Etihad Airways'),
        ('EVA Air'),
        ('Hawaiian Airlines'),
        ('Japan Airlines'),
        ('JetBlue'),
        ('KLM'),
        ('Korean Air'),
        ('Lufthansa'),
        ('Qantas'),
        ('Singapore Airlines'),
        ('Southwest Airlines'),
        ('Spirit Airlines'),
        ('Turkish Airlines'),
        ('Virgin Atlantic'),
        ('Virgin Australia'),
        ('WestJet');

-- Adding airports to cover different cities
INSERT INTO airport (name, city) 
VALUES ('JFK', 'New York'),
       ('PVG', 'Shanghai'),
       ('LAX', 'Los Angeles'),
       ('HND', 'Tokyo'),
       ('LHR', 'London'),
       ('CDG', 'Paris'),
       ('DEL', 'Delhi'),
       ('AKL', 'Auckland'),
       ('SFO', 'San Francisco'),
       ('HKG', 'Hong Kong'),
       ('DXB', 'Dubai'),
       ('AUH', 'Abu Dhabi'),
       ('TPE', 'Taipei'),
       ('HNL', 'Honolulu'),
       ('NRT', 'Tokyo'),
       ('BOS', 'Boston'),
       ('AMS', 'Amsterdam'),
       ('ICN', 'Seoul'),
       ('MUC', 'Munich'),
       ('SYD', 'Sydney'),
       ('SIN', 'Singapore'),
       ('LAS', 'Las Vegas'),
       ('LGA', 'New York'),
       ('BWI', 'Baltimore'),
       ('MIA', 'Miami'),
       ('IST', 'Istanbul'),
       ('YYZ', 'Toronto');

-- Adding customers with diverse destinations and origins
INSERT INTO customer (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth) 
VALUES  ('customer1@example.com', 'Oliver One', 'password1', '123', 'Street 1', 'City 1', 'State 1', '1234567890', 'P12345678', '2025-12-31', 'Country 1', '1990-01-01'),
        ('customer2@example.com', 'Thomas Two', 'password2', '456', 'Street 2', 'City 2', 'State 2', '9876543210', 'P23456789', '2026-12-31', 'Country 2', '1991-01-01'),
        ('customer3@example.com', 'Tim Three', 'password3', '789', 'Street 3', 'City 3', 'State 3', '1111111111', 'P34567890', '2027-12-31', 'Country 3', '1992-01-01'),
        ('customer4@example.com', 'Freddie Four', 'password4', '101', 'Street 4', 'City 4', 'State 4', '2222222222', 'P45678901', '2028-12-31', 'Country 4', '1993-01-01');
       

-- Adding booking agents working for different airlines
INSERT INTO booking_agent (email, password) 
VALUES ('agentA@example.com', 'agentApassword'),
       ('agentB@example.com', 'agentBpassword'),
       ('agentC@example.com', 'agentCpassword');

-- Adding booking agents working for different airlines
INSERT INTO booking_agent_workfor (booking_agent_email, airline_name)
VALUES ("agentA@example.com", 'Delta Air Lines'),
       ('agentA@example.com', 'American Airlines'),
       ('agentB@example.com', 'American Airlines'),
       ('agentB@example.com', 'China Eastern'),
       ('agentC@example.com', 'Delta Air Lines');

-- Adding airplanes to the system (each airline should have about 3~5 airplanes)
INSERT INTO airplane (airline_name, seat_num) 
VALUES ('China Eastern', 300),
       ('China Eastern', 400),
       ('China Eastern', 500),
       ('American Airlines', 300),
       ('American Airlines', 400),
       ('Delta Air Lines', 300),
       ('Delta Air Lines', 400),
       ('Delta Air Lines', 500),
       ('United Airlines', 300),
       ('United Airlines', 400),
       ('Air Canada', 300),
       ('Air Canada', 400),
       ('Air France', 300),
       ('Air France', 400),
       ('Air France', 500),
       ('Air India', 300),
       ('Air India', 400),
       ('Air New Zealand', 300),
       ('Air New Zealand', 400),
       ('Alaska Airlines', 300),
       ('Alaska Airlines', 400),
       ('All Nippon Airways', 300),
       ('All Nippon Airways', 400),
       ('British Airways', 300),
       ('British Airways', 400),
       ('Cathay Pacific', 300),
       ('Cathay Pacific', 400),
       ('Emirates', 300),
       ('Emirates', 400),
       ('Etihad Airways', 300),
       ('Etihad Airways', 400),
       ('EVA Air', 300),
       ('EVA Air', 400),
       ('Hawaiian Airlines', 300),
       ('Hawaiian Airlines', 400),
       ('Japan Airlines', 300),
       ('Japan Airlines', 400),
       ('JetBlue', 300),
       ('JetBlue', 400),
       ('KLM', 300),
       ('KLM', 400),
       ('Korean Air', 300),
       ('Korean Air', 400),
       ('Lufthansa', 300),
       ('Lufthansa', 400),
       ('Qantas', 300),
       ('Qantas', 400),
       ('Singapore Airlines', 300),
       ('Singapore Airlines', 400),
       ('Southwest Airlines', 300),
       ('Southwest Airlines', 400),
       ('Spirit Airlines', 300),
       ('Spirit Airlines', 400),
       ('Turkish Airlines', 300),
       ('Turkish Airlines', 400),
       ('Virgin Atlantic', 300),
       ('Virgin Atlantic', 400),
       ('Virgin Australia', 300);

-- Adding airline staff with different permissions and airlines
-- "Admin" permission staff can create flights, add airplanes/airports, grant permissions
-- "Operator" permission staff can change flight status
-- NULL permission staff can only view flights
INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, airline_name) 
VALUES ('adminStaff1', 'adminPass1', 'Alice', 'Admin', '1975-01-01', 'American Airlines'),
       ('adminStaff2', 'adminPass2', 'Allen', 'Admin', '1976-01-01', 'Delta Air Lines'),
       ('operatorStaff1', 'operatorPass1', 'Oscar', 'Operator', '1985-01-01', 'Delta Air Lines'),
       ('normalStaff1', 'normalPass1', 'Nick', 'Normal', '1995-01-01', 'American Airlines');

-- Add permission to all staff
INSERT INTO airline_staff_permission (username, permission)
VALUES ('adminStaff1', 'Admin'),
       ('adminStaff2', 'Admin'),
       ('adminStaff2', 'Operator'),
       ('operatorStaff1', 'Operator');


-- Generate more flights
INSERT INTO flight (airline_name, departure_time, arrival_time, price, status, airplane_id, arr_airport_name, dept_airport_name)
SELECT 
    a.airline_name,
    DATE_ADD(NOW(), INTERVAL FLOOR(RAND(233) * 100) DAY),
    DATE_ADD(NOW(), INTERVAL FLOOR(RAND(233) * 100) DAY),
    FLOOR(100 + RAND(233) * 900),
    ELT(FLOOR(1 + RAND(233) * 3), 'Upcoming', 'InProgress', 'Delayed'),
    a.airplane_id,
    (SELECT name FROM airport ORDER BY RAND(233) LIMIT 1),
    (SELECT name FROM airport ORDER BY RAND(234) LIMIT 1)
FROM airplane a
ORDER BY RAND(233)
LIMIT 100;

-- Add random day and hour and minute to arrival time
UPDATE flight
SET arrival_time = DATE_ADD(arrival_time, INTERVAL FLOOR(RAND(233) * 60 * 24 * 2) MINUTE);


-- Generate more tickets
INSERT INTO ticket (flight_num, airline_name, customer_email, booking_agent_email, purchase_date)
SELECT 
    f.flight_num,
    f.airline_name,
    (SELECT email FROM customer ORDER BY RAND(233) LIMIT 1),
    CASE WHEN RAND(233) < 0.5 THEN (SELECT ba.email FROM booking_agent ba JOIN booking_agent_workfor baw ON ba.email = baw.booking_agent_email WHERE baw.airline_name = f.airline_name ORDER BY RAND(233) LIMIT 1) ELSE NULL END,
    DATE_SUB(f.departure_time, INTERVAL FLOOR(RAND(233) * 30) DAY)
FROM flight f
ORDER BY RAND(233)
LIMIT 100;
