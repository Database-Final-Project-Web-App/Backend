**Example**

Request

```bash
$ curl -X POST -H "Content-Type: application/json" "http://localhost:5000/api/booking-agent/ticket/purchase" -b cookie.txt -c cookie.txt -d "{\"customer_email\": \"customer3@example.com\", \"flight_num\": 56, \"airline_name\": \"American Airlines\"}"
```

response

```json
{
  "status": "Successfully purchased the ticket."
}
```
