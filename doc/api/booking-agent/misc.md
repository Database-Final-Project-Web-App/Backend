## `/booking-agent/misc/commsion`

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/booking-agent/misc/commission?start_date=2023-01-01&end_date=2024-10-01"
```

response

```json
{
  "avg_commission": "95.4000000",
  "commission": "190.800",
  "num_tickets": 2
}
```

## `/booking-agent/misc/top-customer`

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/booking-agent/misc/top-customer?start_date=2023-01-01&end_date=2024-10-01&limit=5"
```

response

```json
{
  "top_commission_customer": [
    {
      "commission": "190.800",
      "customer_email": "customer3@example.com"
    }
  ],
  "top_tickets_customer": [
    {
      "customer_email": "customer3@example.com",
      "num_tickets": 2
    }
  ]
}
```