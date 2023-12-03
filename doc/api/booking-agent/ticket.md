# Booking agent purchase ticket

## `/booking-agent/ticket/purchase`

>http://localhost:5000/api/booking-agent/ticket/purchase

**Request**: `POST`

Purchase a ticket for a customer through the booking agent

**Request Parameters**

**Input Type**: `application/json`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| flight_num | number | The flight number | yes | |
| customer_email | string | A specific customer email | yes | |
| airline_name | string | The airline name | yes | |

**json response**

Root Objects:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | Purchase successful or not | |
| message | string | the error message or successful message | |

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
