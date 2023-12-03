# Customer purchase ticket

## `/customer/ticket/purchase`

>http://localhost:5000/api/customer/ticket/purchase

**Request**: `POST`

Customer directly purchase a ticket

**Request Parameters**

**Input Type**: `application/json`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| flight_num | number | The flight number | yes | |
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
curl -X POST -b cookie.txt -c cookie.txt "http://localhost:5000/api/customer/ticket/purchase" -H "Content-Type: application/json" -d "{\"flight_num\": 1, \"airline_name\": \"Air Canada\"}"
```

Response

```json
{
    "status": "success",
	"message": "Ticket purchased."
}
```
