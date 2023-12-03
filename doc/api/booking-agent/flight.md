# booking agent flight

## `/booking-agent/flight/my`

>http://localhost:5000/api/booking-agent/flight/my

View all flights bought through the booking agent

**Request**: `POST`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| flight_num | number | The flight number | no | |
| airline_name | string | The airline name | no | |
| customer_email | string | A specific customer email | no | |
| departure_name | string | The departure airport name | no | |
| arrival_time | string | The arrival time | no | |
| price | number | The price of the flight | no | |
| status | string | The status of the flight | no | Default: Upcoming|
| airplane_id | number | The airplane id | no | |
| arr_airport_name | string | The arrival airport name | no | |
| dep_airport_name | string | The departure airport name | no | |
| arr_city | string | The arrival city | no | |
| dept_city | string | The departure city | no | |
| ticket_id | int | search for one specific ticket | no | |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flights | array | An array of flight objects | |

`flights[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flight_num | int | The flight number | |
| airline_name | string | The airline name | |
| departure_time | string | The departure time | format: `YYYY-MM-DD HH:MM` |
| arrival_time | string | The arrival time | format: `YYYY-MM-DD HH:MM` |
| price | float | The price of the flight | |
| status | string | The status of the flight | |
| airplane_id | int | The airplane id | |
| arr_airport_name | string | The arrival airport name | |
| dep_tairport_name | string | The departure airport name | |
| arr_city | string | The arrival city | |
| dept_city | string | The departure city | |
| ticket_id | int | Ticket ID | |
| customer_email | string | email of specific customer| |

**Example**:

Request

```bash
$ curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{}" "http://localhost:5000/api/booking-agent/flight/my"
```

Response

```json
{
  "flights": [
    {
      "airline_name": "American Airlines",
      "airplane_id": 4,
      "arr_airport_name": "LHR",
      "arr_city": "LHR",
      "arrival_time": "Wed, 06 Mar 2024 16:24:30 GMT",
      "booking_agent_email": "agentA@example.com",
      "customer_email": "customer3@example.com",
      "departure_time": "Wed, 06 Mar 2024 08:26:30 GMT",
      "dept_airport_name": "SFO",
      "dept_city": "San Francisco",
      "flight_num": 56,
      "price": "954.00",
      "purchase_date": "Sat, 02 Mar 2024 08:26:30 GMT",
      "status": "Delayed",
      "ticket_id": 8
    }
  ]
}
```