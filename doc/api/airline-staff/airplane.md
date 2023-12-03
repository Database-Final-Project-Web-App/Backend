##`/airline-staff/airplane/add`

**Example**

Resuqet

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/airplane/add" -d"{\"seat_num\": 350}"
```

Response

```json
{
  "status": "success"
}
```