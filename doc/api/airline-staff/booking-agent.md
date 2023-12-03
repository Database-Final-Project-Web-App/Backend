# Top booking agents

## `/airline-staff/booking-agent/all`

Method: `GET`

**Example**

Request

```bash
curl -X GET -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/booking-agent/all?limit=5"
```

Response

```json
{
  "Top 5 booking agent based on the commission received for last year": [
    [
      "agentA@example.com",
      "95.400"
    ]
  ],
  "Top 5 booking agent based on the number of tickets for last month": [
    [
      "agentA@example.com",
      1
    ]
  ],
  "Top 5 booking agent based on the number of tickets for last year": [
    [
      "agentA@example.com",
      1
    ]
  ]
}
```

# Add Booking agent

## `/airline-staff/booking-agent/add`

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/booking-agent/add" -d"{\"booking_agent_email\": \"agentB@example.com\"}"
```

Response

```json
{
  "status": "success"
}
```