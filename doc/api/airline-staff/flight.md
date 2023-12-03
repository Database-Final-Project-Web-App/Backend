# Airline staff flight

## `/airline-staff/flight/my`

>http://localhost:5000/api/airline-staff/flight/my

View all upcoming flight

**Request**: `POST`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| flight_num | number | The flight number | no | |
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

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{\"start_date\": \"2023-12-01\", \"end_date\": 
\"2024-01-01\"}" "http://localhost:5000/api/airline-staff/flight/my"
```

response

```json
{
  "flights": [
    {
      "airline_name": "American Airlines",
      "airplane_id": 5,
      "arr_airport_name": "ICN",
      "arr_city": "ICN",
      "arrival_time": "Thu, 07 Dec 2023 10:25:30 GMT",
      "booking_agent_email": "agentB@example.com",
      "customer_email": "customer2@example.com",
      "departure_time": "Thu, 07 Dec 2023 08:26:30 GMT",
      "dept_airport_name": "NRT",
      "dept_city": "Tokyo",
      "flight_num": 2,
      "price": "139.00",
      "purchase_date": "Wed, 06 Dec 2023 08:26:30 GMT",
      "status": "Upcoming",
      "ticket_id": 1
    },
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
      "purchase_date": "Sun, 03 Dec 2023 11:42:54 GMT",
      "status": "Delayed",
      "ticket_id": 67
    }
  ]
}
```

## `/airline-staff/flight/create`

>http://localhost:5000/api/airline-staff/flight/create

Create a new flight for the airline

**Request**: `POST`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| departure_name | string | The departure airport name | no | |
| arrival_time | string | The arrival time | yes | |
| price | number | The price of the flight | yes | |
| status | string | The status of the flight | yes | Default: Upcoming|
| airplane_id | number | The airplane id | yes | |
| arr_airport_name | string | The arrival airport name | yes | |
| dep_airport_name | string | The departure airport name | yes | |

**Json Response**

Root object:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | create new flight successfully or not | |

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{\"airline_name\": \"China Eastern\", \"airplane_id\": 4, \"departure_time\": \"2024-01-15 10:30:00\", \"arrival_time\": \"2024-01-15 19:45:00\", \"price\": 372.00, \"status\": \"Upcoming\", \"arr_airport_name\": \"NRT\", \"dept_airport_name\": \"BOS\"}" "http://localhost:5000/api/airline-staff/flight/create"
```

response

```json
{
  "status": "success"
}
```

## `/airline-staff/flight/change-status`

>http://localhost:5000/api/airline-staff/flight/change-status

**Request**: `POST`

Change status for specific flight in the airline. Only staff with "Operator" permission can do this.

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| flight_num | int | the flight number the staff wants to change | yes | |
| status | string | status wants to change into | yes| can only be "Upcoming", "Inprogress", "Delayed" |

**json responce**

Root Objects:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | change status successful or not | |
| message | string | the error message or successful message | |

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/flight/change-status" -d"{\"flight_num\": 17, \"status\": \"Upcoming\"}"
```

Response

```json
{
  "status": "success"
}
```