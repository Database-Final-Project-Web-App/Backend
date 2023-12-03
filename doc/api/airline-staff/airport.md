## `/airline-staff/airport/add`

>http://localhost:5000/api/airline-staff/airport/add

**Request Parameters**

**Input Type**: `application/json`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| name | string | Name of the added airport | yes | |
| city | string | City that the airport located | yes | |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | Whether the operation successful or not | |
| message | string | the error message or successful message | |

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