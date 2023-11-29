# Public Information about Flight

## `/public/flight/search`

> http://localhost:5000/api/public/flight/search 

**Request**: `POST`

Search for flights based on the given parameters.

**Request Parameters**

**Input Type**: `application/json`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| flight_id | number | The flight number | no | |
| airline_name | string | The airline name | no | |
| departure_name | string | The departure airport name | no | |
| arrival_time | string | The arrival time | no | |
| price | number | The price of the flight | no | |
| status | string | The status of the flight | no | Default: Upcoming|
| airplane_id | number | The airplane id | no | |
| arr_airport_name | string | The arrival airport name | no | |
| dep_airport_name | string | The departure airport name | no | |


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




**Example**:

Request

```bash
# search for flights with price between 100 and 280
curl -X POST -H "Content-Type: application/json" -d "{\"price\": [100, 280]}" http://localhost:5000/api/public/flight/search
```

Response

```json
{
  "flights": [
	{
	  "airline_name": "Delta",
	  "airplane_id": 1,
	  "arrival_time": "2019-12-01 12:00",
	  "arr_airport_name": "SFO",
	  "departure_time": "2019-12-01 10:00",
	  "dep_airport_name": "LAX",
	  "flight_id": 1,
	  "price": 150.0,
	  "status": "upcoming"
	},
	{
	  "airline_name": "Delta",
	  "airplane_id": 1,
	  "arrival_time": "2019-12-01 12:00",
	  "arr_airport_name": "SFO",
	  "departure_time": "2019-12-01 10:00",
	  "dep_airport_name": "LAX",
	  "flight_id": 2,
	  "price": 240.0,
	  "status": "upcoming"
	}
  ]
}
```


