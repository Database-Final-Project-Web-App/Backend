# Top booking agents

## `/airline-staff/booking-agent/all`

**Request**: `GET`

>http://localhost:5000/api/airline-staff/booking-agent/all

Show the top booking agents works for the airline the staff works for, based on the commission received and the number of tickets sold for the past year and month.

Request Parameter: Query Parameters

**Input Type**: Static Values

Root object:
| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| limit | int | The top limit booking agents wants to see | no | |

**Json Response**

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- | 
| Top 5 booking agent based on the commission received for last year | array | Show the top agents and the commission received from them for last year | |
| Top 5 booking agent based on the number of tickets for last month | array | The top agents and the number of tickets they sold last month| |
| Top 5 booking agent based on the number of tickets for last year | array | Top agents and the number of tickets they sold last year | |


**Example**

Request

```bash
curl -X GET -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/booking-agent/all?limit=5"
```

Response

```json
{
  "Top 5 booking agent based on the commission received for last year": [
    [
      "agentA@example.com",
      "95.400"
    ]
  ],
  "Top 5 booking agent based on the number of tickets for last month": [
    [
      "agentA@example.com",
      1
    ]
  ],
  "Top 5 booking agent based on the number of tickets for last year": [
    [
      "agentA@example.com",
      1
    ]
  ]
}
```

# Add Booking agent

## `/airline-staff/booking-agent/add`

>http://localhost:5000/api/airline-staff/booking-agent/add

Add booking agent that can work for the airline which the staff works for.

**Request Parameters**

**Input Type**: `application/json`

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| booking_agent_eamil | string | The booking agent the staff wants to add | yes | |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | Whether the operation successful or not | |
| message | string | the error message or successful message | |

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/booking-agent/add" -d"{\"booking_agent_email\": \"agentB@example.com\"}"
```

Response

```json
{
  "status": "success"
}
```