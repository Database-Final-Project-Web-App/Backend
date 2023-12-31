# API Doc

This is the documentation for the api of the backend server of the Airline Ticket Reservation System. 

## About

The api is essentially used to execute certain sql query. For example, if the backend server is running at `localhost:5000`, we can define an api for fetching all tickets by defining a trigger (function) at the routing path `/api/data/all-ticket` that executes the sql query `SELECT * FROM ticket;`. This way, when the user send HTTP GET request to `localhost:5000/api/data/all-ticket`, he/she would get the table of all tickets (as a json object). This is done with the following flask code.

```python
@app.route("/api/data/all-ticket")
def get_allTicket():	
	# for simplicity, we ignore argument, query template, and exception handling
	result = db.execute_query("SELECT * FROM ticket;")
	return jsonify(result)
```

The API is loosely categorized by 

1. user role

   e.g. `.../customer/...`

2. object it acts upon (the table to be query). 

   e.g. `.../flight/...`

## API Design

This is a list of content for each api endpoint. The details of each endpoint is documented in a separate page, which is linked in the list below. 
- For an annotated example, see [here](/app/api/public/flight/flight_bp.py). 
- [Developer] For an example doc, see [here](/doc/api/public/flight.md).

### API for General Features

These api's are for general features that works for all types of users. The input and output of these api shouldn't depend on the user role. 

1. **Public Information**

    This group of API is to get public information. It should only accept `GET` request, and the result should be independent from user role.

   - `/public` 

      - [`/flight`](/doc/api/public/flight.md)

        <!-- - `GET /:flight_id`: 
          Get the detailed info of a specific flight, could be used to render a dedicated page for that flight -->

        - `POST /search`: Allows searching for flights

1. **Authentication**

   - `/auth`

     - [`POST /register`](/doc/api/auth/register.md): 
       
       Register a new user.

     - [`POST /login`](/doc/api/auth/login.md):
  
       Authenticate and log in a user.

     - [`POST /logout`](/doc/api/auth/logout.md):
    
       Log out the currently authenticated user.

### API for Role-Based Features

These api's are for features with one of the following properties
- is only accessible to certain user role (e.g. update flight status)
- has different behavior for users with different roles (e.g. register as customer / booking agent / airline staff)

1. **Customer:**
   
   - `/customer`

     - [`/flight`](/doc/api/customer/flight.md)

       - `POST /my`: Retrieve flights for the authenticated user 

     - [`/ticket`](/doc/api/customer/ticket.md)

       - `POST /purchase`: Purchase tickets for the authenticated user (directly without an agent).

     - [`misc`](doc/api/customer/misc.md)

       - `GET /spending`: Retrieve spending information for the authenticated user.

2. **Booking Agent:**

   - `/booking-agent`

     - [`/flight`](/doc/api/booking-agent/flight.md)

       - `POST /my`: Retrieve flights for the authenticated user 

     - [`/ticket`](/doc/api/booking-agent/ticket.md)

       - `POST /purchase`: Purchase tickets for the authenticated user (via an agent).

     - [`/misc`](/doc/api/booking-agent/misc.md)

       - `GET /commission`: Retrieve commission information for the authenticated booking agent.

       - `GET /top-customer`: Retrieve top customers for the authenticated booking agent.

3. **Airline Staff:**

   Since airline staff are very different from customers and booking agents, and airline staff has its own access control to deal with, we create separate family of api endpoints for them.

   - `/airline-staff`

     - [`/flight`](/doc/api/airline-staff/flight.md)

       - `GET /my`: Retrieve flights for the authenticated airline staff.

       - `POST /create`: Create a new flight.

       - `POST /change-status`: Change the status of a specific flight.

     - [`/airplane`](/doc/api/airline-staff/airplane.md)

        - `POST /add`: Add a new airplane to the system.

     - [`/airport`](/doc/api/airline-staff/airport.md)

        - `POST /add`: Add a new airport to the system.

     - [`/booking-agent`](/doc/api/airline-staff/booking-agent.md)

        - `GET /all`: Retrieve a list of all booking agents.

        - `POST /add`: Add new booking agents.

     - [`/misc`](/doc/api/airline-staff/misc.md)

        - `GET /frequent-customer`: Retrieve a list of frequent customers.

        - `GET /report`: Retrieve a report.

        - `GET /revenue-comparison`: Compare revenue earned.

        - `GET /top-destination`: Retrieve top destinations.

        - `POST /grant-permission`: Grant new permissions to users.

## Design Tips

1. Separation of API design and API implementation

    We should separate API design from API implementation. Two different API could share the same implementation. 

    For example, the action `login` for customer and for booking agent corresponds to two different apis, but share pretty much the same implementation

    ```python
    def purchase(query_param: dict):
      """
      Update database to purchase ticket. Return error if needed

      :param: query_param
      return: 
      """
      result = None
      # implementation detail
      purchase_query_template = """
        INSERT INTO ticket (flight_id, airline_name, customer_email, booking_agent_email) 
        VALUES ({flight_id}, {airline_name}, {customer_email}, {booking_agent_email})
      """
      db.execute_query(purchase_query_template.format(**query_param))
      return result


    @app.route("/api/customer/ticket/purchase", methods=["GET"])
    def customer_purchase_ticket():
      # Check if client is customer
      if session.get("user_type") != "customer":
        return "only customer can use this api!", 
      # Obtain parameters from request
      # Diff: For customer
      # - we get `customer_email` from session data
      # - we set `booking_agent_email` to None
      query_param = {
        "customer_email": session.get("username"),
        "flight_id": request.args.get("flight_id"),
        "airline_name": request.args.get("airline_name"),
        "booking_agent_email": None,
      }
      # Same: use the purchase function
      result = purchase(query_param)
      # make response
      if result is None:
        return jsonify({"message": "Failed to buy ticket due to failure of database update"}), 500
      return result 


    @app.route("/api/booking-agent/ticket/purchase")
    def bookingAgent_purchase_ticket():
      # Check if client is booking agent
      if session.get("user_type") != "booking-agent":
        return "only booking agent can use this api!", 
      # Obtain parameters from request
      # Diff: For booking agent
      # - we get `customer_email` from url argument
      # - we get `booking_agent_email` from session data
      query_param = {
        "customer_email": request.args.get("customer_email"),
        "flight_id": request.args.get("flight_id"),
        "airline_name": request.args.get("airline_name"),
        "booking_agent_email": session.get("username"),
      }
      # Same: use the purchase function
      result = purchase(query_param)
      # make response
      if result is None:
        return jsonify({"message": "Failed to buy ticket due to failure of database update"}), 500
      return result 
    ```

    A previous rejected design is use a single `/user/flight/my` and separate customer and booking agent with an if statement. This would require a lenthy function for `/user/flight/my`. It also force us to catoegorize feature api into three groups: `/user`, `/customer`, and `/booking-agent`, which adds unnecessary burden for api design.

2. Make the Implementation Modular 

    This design brings **reuseability** and **composibility**

    1. In the example used in 1., we design a separate function `purchase(query_param: dict)` (a module), and reuse this function in the implementation of two different api.

    2. We can compose different module to implement an api. For example, TODO:

