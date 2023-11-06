# Public Information about Flight

## `/public/flight/search`

> http://localhost:5000/api/public/flight/search 

**Request**: `GET`

Search for flights using url parameters.

**Parameter**

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| airline_name | | | | |
| departure_name | | | | |
| arrival_time | | | | |
| price | | | | |
| arr_airport_name | string | The arrival airport name | no | if not given, match all |
|  | | | | |


**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flights | array | An array of flight objects | |

**Example**:

```bash
curl -X GET http://localhost:5000/api/public/flight/search?from=Toronto&to=Vancouver&date=2020-12-01
```


