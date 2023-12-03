##`/airline-staff/airport/add`

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/airport/add" -d"{\"name\": \"SHA\", \"city\": \"Shanghai\"}"
```

Response

```json
{
  "status": "success"
}
```