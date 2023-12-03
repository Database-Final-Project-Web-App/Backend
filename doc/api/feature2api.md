## Match Feature to API

1. View Public Info: All users, whether logged in or not, can

   1. Search for upcoming flights based on source city/airport name, destination city/airport name, date.

      > `POST /public/flight/search`

   2. Will be able to see the flights status based on flight number, arrival/departure date.

      > `POST /public/flight/search`

2. Register: 3 types of user registrations (Customer, Booking agent, Airline Staff) option via forms.

   > `POST /auth/register`

3. Login: 3 types of user login (Customer, Booking agent, Airline Staff). User enters their username (email address will be used as username), x, and password, y, via forms on login page. This data is sent as POST parameters to the login-authentication component, which checks whether there is a tuple in the Person table with username=x and the password = md5(y).

   > `POST /auth/login`

   1. If so, login is successful. A session is initiated with the member’s username stored as a session variable. Optionally, you can store other session variables. Control is redirected to a component that displays the user’s home page.

   2. If not, login is unsuccessful. A message is displayed indicating this to the user.
   
   Note: In real applications, members’ passwords are stored as md5/other hashes, not as plain text. This keeps the passwords more secure, in case someone is able to break into the system and see the passwords. You can perform the hash using MySQL’s md5 function or a library provided with your host language. Once a user has logged in, reservation system should display his/her home page. Also, after other actions or sequences of related actions, are executed, control will return to component that displays the home page.

   On error, the home page should display:

      * Error message if the previous action was not successful,

      * Some mechanism for the user to choose the use case he/she wants to execute. You may choose to provide links to other URLS that will present the interfaces for other use cases, or you may include those interfaces directly on the home page. 

      * Any other information you’d like to include. For example, you might want to show customer's upcoming flights information on the customer's home page, or you may prefer to just show them when he/she does some of the following use cases.

## Customer use cases:

After logging in successfully a user(customer) may do any of the following use cases:

1. View My flights: Provide various ways for the user to see flights information which he/she purchased. The default should be showing for the upcoming flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name or city name etc.

   > `POST /customer/flight/my`

2. Purchase tickets: Customer chooses a flight and purchase ticket for this flight. You may find it easier to implement this along with a use case to search for flights.

   > `POST /customer/ticket/purchase`

3. Search for flights: Search for upcoming flights based on source city/airport name, destination city/airport name, date.

   > `GET /public/flight/search`

4. Track My Spending: Default view will be total amount of money spent in the past year and a bar chart showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to view total amount of money spent within that range and a bar chart showing month wise money spent within that range. (Bar chart is optional, you can choose to represent the data anyway you like)

   > `GET /customer/misc/spending`

5. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

   > `POST /auth/logout`

## Booking agent use cases:

After logging in successfully a booking agent may do any of the following use cases:

1. View My flights: Provide various ways for the booking agents to see flights information for which he/she purchased on behalf of customers. The default should be showing for the upcoming flights. Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name and/or city name etc to show all the flights for which he/she purchased tickets.

   > `POST /booking-agent/flight/my`

2. Purchase tickets: Booking agent chooses a flight and purchases tickets for other customers giving customer information. You may find it easier to implement this along with a use case to search for flights. Notice that as described in the previous assignments, the booking agent may only purchase tickets from airlines they work for.

   > `POST /booking-agent/ticket/purchase`

3. Search for flights: Search for upcoming flights based on source city/airport name, destination city/airport name, date.

   > `GET /public/flight/search`

4. View my commission: Default view will be total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. He/she will also have option to specify a range of dates to view total amount of
commission received and total numbers of tickets sold.

   > `GET /booking-agent/misc/commission`

5. View Top Customers: Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and top 5 customers based on amount of commission received in the last year. Show a bar chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. Show another bar chart showing each of these 5 customers in x-axis and amount commission received in y- axis. (Again, UI/bar chart is optional, the important factor is that you are able to retrieve and display the data.)

   > `GET /booking-agent/misc/top-customer`

6. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

   > `POST /auth/logout`

## Airline Staff use cases:

After logging in successfully an airline staff may do any of the following use cases:

1. View My flights: Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.

   > `POST /airline-staff/flight/my`

2. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days.

   > `POST /airline-staff/flight/create`

3. Change Status of flights: He or she changes a flight status (from upcoming to in progress, in progress to delayed etc) via forms. The application should prevent unauthorized users or staffs without "Operator" permission from doing this action.

   > `POST /airline-staff/flight/change-status`

4. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. In the confirmation page, she/he will be able to see all the airplanes owned by the airline he/she works for.

   > `POST /airline-staff/airplane/add`

5. Add new airport in the system: He or she adds a new airport, providing all the needed data, via forms. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. (Additional requirement: Airline Staff with "Admin" permission will be able to add new airports into the system for the airline they work for.)

   > `POST /airline-staff/airport/add`

6. View all the booking agents: Top 5 booking agents based on number of tickets sales for the past month and past year. Top 5 booking agents based on the amount of commission received for the last year.

   > `GET /airline-staff/booking-agent`

7. View frequent customers: Airline Staff will also be able to see the most frequent customer within the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.

   > `GET /airline-staff/misc/frequent-customer`

8. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise tickets sold in a bar chart.

   > `GET /airline-staff/misc/report`

9.  Comparison of Revenue earned: Draw a pie chart for showing total amount of revenue earned from direct sales (when customer bought tickets without using a booking agent) and total amount of revenue earned from indirect sales (when customer bought tickets using booking agents) in the last month and last year.
    > `GET /airline-staff/misc/revenue-comparison`

10. View Top destinations: Find the top 3 most popular destinations for last 3 months and last year.

    > `GET /airline-staff/misc/top-destination`

11. Grant new permissions: Grant new permissions to other staffs in the same airline. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. Initially there should be a staff with "Admin" permission in the database for each airline. Airline staffs registered through the application DO NOT have any permissions at beginning. (Additional requirement: Airline Staff with "Admin" permission will be able to grant new permissions to staffs in the same airline.)

    > `GET /airline-staff/misc/grant-permission`

12. Add booking agents: Add booking agents that can work for this airline, providing their email address. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. A booking agent cannot work for any airline (thus cannot purchase tickets) until any staff add then through this action. (Additional requirement: Airline Staffs with "Admin" permission will be able to add booking agents that can work for their airline.)

    > `GET /airline-staff/booking-agent/add`

13. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

    > `POST /auth/logout`