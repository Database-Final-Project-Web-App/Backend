**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/customer/misc/spending?start_date=2023-01-01&end_date=2024-01-01"
```

Result

```json
{
  "end_date": "2024-01-01",
  "monthly_spending": {
    "2023-11": 150.0,
    "2023-12": 1405.0
  },
  "start_date": "2023-01-01",
  "total_spending": 1555.0
}
```