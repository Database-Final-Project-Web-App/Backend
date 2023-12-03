# Booking agent misc functions

## `/booking-agent/misc/commission`

>http://localhost:5000/api/booking-agent/misc/commission

**Request**: `GET`

Find total commission, average commision and number of tickets during a specific time range.

**Request Parameters** Query Parameters

**Input Type**: Static Values

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- |
| start_date | string | The beginning of the time range | No | format: `YYYY-MM-DD HH:MM` |
| end_date | string | The end of the time range | No | format: `YYYY-MM-DD HH:MM`, defaulted current date |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| avg_commission | string | Total commission divided by the number of tickets | |
| commission | string | Total commission | |
| num_tickets | num | Number of tickets bought through the booking agent | |

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/booking-agent/misc/commission?start_date=2023-01-01&end_date=2024-10-01"
```

response

```json
{
  "avg_commission": "95.4000000",
  "commission": "190.800",
  "num_tickets": 2
}
```

## `/booking-agent/misc/top-customer`

>http://localhost:5000/api/booking-agent/misc/top-customer

**Request**: `GET`

Find top customer based on commission and number of ticket he/she bought during a specific time range.

**Request Parameters** Query Parameters

**Input Type**: Static Values

Root object

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- |
| start_date | string | The beginning of the time range | No | format: `YYYY-MM-DD HH:MM` |
| end_date | string | The end of the time range | No | format: `YYYY-MM-DD HH:MM`, defaulted current date |
| limit | int | top number want to see | No | Default to 5 |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| top_commission_customer | array | Total commission recieved from the top customers | |
| top_tickets_customer | array | Number of tickets bought by top customers | |

`top_commission_customer[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| commission | string | total commission | |
| customer_email | string | email of top customer | |

`top_tickets_customer[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| num_tickets | int | Number of tickets the customer bought through the agent| |
| customer_email | string | email of top customer | |

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/booking-agent/misc/top-customer?start_date=2023-01-01&end_date=2024-10-01&limit=5"
```

response

```json
{
  "top_commission_customer": [
    {
      "commission": "190.800",
      "customer_email": "customer3@example.com"
    }
  ],
  "top_tickets_customer": [
    {
      "customer_email": "customer3@example.com",
      "num_tickets": 2
    }
  ]
}
```