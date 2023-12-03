**Example**:

Request

```bash
$ curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{}" http://localhost:5000/api/booking-agent/flight/my
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