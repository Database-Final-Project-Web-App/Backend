## `/airline-staff/airplane/add`

>http://localhost:5000/api/airline-staff/airplane/add

Add a new airplane for the airline

**Request Parameters**

**Input Type**: `application/json`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| seat_num | int | The number of seats the airplane has | yes | |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | Whether the operation successful or not | |
| message | string | the error message or successful message | |

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