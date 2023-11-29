# Feature to api and SQL
## 
1. View Public Info: All users, whether logged in or not, can

   1. Search for upcoming flights based on source city/airport name, destination city/airport name, date.
         > `POST /public/flight/search`

      ```mysql-sql
      WITH flight_city AS
	   (SELECT flight.*, a1.city AS dept_city, a2.name AS arr_city
      FROM airport AS a1, airport AS a2, flight
      WHERE a1.name = flight.dept_airport_name 
      AND a2.name = flight.arr_airport_name)
      SELECT *
      FROM flight_city
      WHERE {flight_id}
      AND {airline_name}
      AND {arrival_time}
      AND {departure_time}
      AND {price}
      AND {status}
      AND {airplane_id}
      AND {arr_airport_name}
      AND {dept_airport_name}
      AND {arr_city}
      AND {dept_city}
      ```
   2. Will be able to see the flights status based on flight number, arrival/departure date.
      ```mysql-sql
      SELECT * FROM flight WHERE flight_idber = 'flight_idber' AND departure_time >= 'date';
      ```
2. Register: 3 types of user registrations (Customer, Booking agent, Airline Staff) option via forms.

    | User Type | Registration Form |
    | --------- | ----------------- |
    | Customer  | Name, Email, Password, Building Number, Street, City, State, Phone Number, Passport Number, Passport Expiration Date |
    | Booking Agent | Booking Agent ID, Email, Password, Airline Name|
    | Airline Staff | Username, First Name, Last Name, Date of Birth, Airline Name, Permission |

    1. Customer Registration
        ```mysql-sql
         SELECT * FROM customer WHERE email = email and password = password
        ```
       If the customer is not registered, then insert the customer information into the database.
        ```mysql-sql
        INSERT INTO customer VALUES (email, password, name, building_number, street, city, state, phone_number, passport_number, passport_expiration_date)
        ```
    2. Booking Agent Registration
       ```mysql-sql
       SELECT * FROM customer WHERE email = email and password = password
         ```
         If the booking agent is not registered, then insert the booking agent information into the database.
       ```mysql-sql
       INSERT INTO booking_agent VALUES (email, booking_agent_id, password, airline_name)
       ```

    3. Airline Staff Registration
        ```mysql-sql
        SELECT * FROM airline_staff WHERE username = username and password = password
        ```
        If the airline staff is not registered, then insert the airline staff information into the database.
       ```mysql-sql
       INSERT INTO airline_staff VALUES(username, password, first_name, last_name, date_of_birth, permission, airline_name)
       ```
3. Login: 3 types of user login (Customer, Booking agent, Airline Staff) option via forms.
    
   | User Type | Login Form |
   | --------- | ---------- | 
   | Customer  | Email, Password |
   | Booking Agent | Email, Password |
   | Airline Staff | Username, Password |
    
   1. Customer Login
      ```mysql-sql
      SELECT * FROM customer WHERE email = email and password = password
      ```
   2. Booking Agent Login
      ```mysql-sql
      SELECT * FROM booking_agent WHERE email = email and password = password
      ```
   3. Airline Staff Login
       ```mysql-sql
      SELECT * FROM airline_staff WHERE username = username and password = password
      ```
## Customer use cases:

After logging in successfully a user(customer) may do any of the following use cases:

1. View My flights: Provide various ways for the user to see flights information which he/she purchased. The default should be showing for the upcoming flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name or city name etc.
    ```mysql-sql
   WITH flight_city AS (SELECT flight.*, a1.city AS dept_city, a2.name AS arr_city FROM airport as a1, airport as a2, flight WHERE a1.name = flight.dept_airport_name AND a2.name = flight.arr_airport_name;)
    SELECT * FROM ticket JOIN flight_city USING (flight_id) WHERE {airline_name} AND {departure_time} AND {arrival_time} AND {price} AND {status} AND {city} AND {departure_airport} AND {arrival_airport}
    ```