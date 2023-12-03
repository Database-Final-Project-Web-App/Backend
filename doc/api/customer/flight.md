# Information about Customer's Flight

## `/customer/flight/my`

> http://localhost:5000/api/customer/flight/my

**Request**: `POST`

Retrieve all flights bought by the logged in customer.

**Parameter**

No parameter needed from GET request. The SQL query only needs customer email, which is stored in session data.

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flights | array | An array of flight objects | |

`flights[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flight_id | int | The flight number | |
| airline_name | string | The airline name | |
| departure_time | string | The departure time | format: `YYYY-MM-DD HH:MM` |
| arrival_time | string | The arrival time | format: `YYYY-MM-DD HH:MM` |
| price | float | The price of the flight | |
| status | string | The status of the flight | |
| airplane_id | int | The airplane id | |
| arr_airport_name | string | The arrival airport name | |
| dep_airport_name | string | The departure airport name | |

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{}" http://localhost:5000/api/customer/flight/my
```
$