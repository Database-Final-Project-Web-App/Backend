## `/airline-staff/flight/my`

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{\"start_date\": \"2023-12-01\", \"end_date\": 
\"2024-01-01\"}" http://localhost:5000/api/airline-staff/flight/my
```

Result

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

##`/airline-staff/flight/create`

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{\"airline_name\": \"China Eastern\", \"airplane_id\": 4, \"departure_time\": \"2024-01-15 10:30:00\", \"arrival_time\": \"2024-01-15 19:45:00\", \"price\": 372.00, \"status\": \"Upcoming\", \"arr_airport_name\": \"NRT\", \"dept_airport_name\": \"BOS\"}" http://localhost:5000/api/airline-staff/flight/create
```

Result

```json
{
  "status": "success"
}
```

##`/airline-staff/flight/:flight_id/status`

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