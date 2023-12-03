# Top frequent customer

## `/airline-staff/misc/frequent-customer`

> http://localhost:5000/api/airline-staff/misc/frequent-customer

**Request**: `GET`

Find top frequent customer in the airline which the staff works for. The frequency can be derived from the number of tickets the customer bought in the specific range of time.

**Request Parameters** Query Parameters

**Input Type**: Static Values

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- |
| limit | int | The number of top customer you want to see| No | Defaulted to list all


**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flights | Dictionary | An array of flight objects for specific customer | |
|top_frequent_customers | Array | An array of customer_email and tickets number | |

`top_frequent_customers[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| customer_email | string | the email of top customer| |
| num_tickets | int | the number of tickets the customer bought | |

`flights[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flight_customer | array | all flights of the customer| |

`flights_customer[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| flight_id | int | The flight number | |
| airline_name | string | The airline name | |
| purchase_date | string | purchase date | format: `YYYY-MM-DD HH:MM` |
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
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/frequent-customer?limit=5"
```

Response

```json
{
  "flights": [],
  "top_frequent_customers": "No customer found"
}
```

# View report

## `/airline-staff/misc/report`

> http://localhost:5000/api/airline-staff/misc/report

**Request**: `GET`

get report of total amounts of ticket and the number of tickets sold based on range of dates. Month wise tickets sold data.

**Request Parameters** Query Parameters

**Input Type**: Static Values

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- |
| start_date | string | The beginning of the time range | No | format: `YYYY-MM-DD HH:MM` |
| end_date | string | The end of the time range | No | format: `YYYY-MM-DD HH:MM`, defaulted current date |

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| start_date | string | The beginning of the time range | format: `YYYY-MM-DD HH:MM` |
| end_date | string | The end of the time range | format: `YYYY-MM-DD HH:MM`, defaulted current date |
| Monthly_report_tickets | Dictionary | month wise amount and number of tickets | |
| Total amount of tickets | Dictionary | total amount and total number of tickets | |


`Monthly_report_tickets[i]` object:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| year-month | array | monthly ticket sales information | |

`monthly data[i]` object:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| Total amount | float | Month wise amount | |
| number of tickets | float | month wise number of tickets sold | |

`Monthly_report_tickets[i]` object:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| Number of tickets sold | float | Total number of tickets sold | |
| Total amount | float | Total amount | |



**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/report?start_date=2023-06-01&end_date=2024-06-01"
```

Response

```json
{
  "Monthly_report_tickets": {
    "2023-12": {
      "Total amount": 725.0,
      "number of tickets": 2.0
    },
    "2024-01": {
      "Total amount": 569.0,
      "number of tickets": 1.0
    }
  },
  "Total amount of tickets": {
    "Number of tickets sold": 3.0,
    "Total amount": 1294.0
  },
  "end_date": "2024-06-01",
  "start_date": "2023-06-01"
}
```

# Revenue-comparison

## `/airline-staff/misc/revenue-comparison`

> http://localhost:5000/api/airline-staff/misc/revenue-comparison

**Request**: `GET`

Return total amount of both direct and indirect earning ways in the last month and last year

**Json Response**

Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| booking_revenue_last_month | float | Total amount of revenue earned from indirect sales in the last month (customer buy tickets through booking agents) | |
| booking_revenue_last_year | float | Total amount of revenue earned from indirect sales (customer buy tickets through booking agents) in the last month | |
| direct_revenue_last_month | float | Total amount of revenue earned from direct sales in the last month (customer buy tickets without booking agents) | |
| direct_revenue_last_year | float | Total amount of revenue earned from direct sales in the last year (customer buy tickets without booking agents) | |

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/revenue-comparison"
```

Response

```json
{
  "booking_revenue_last_month": 0.0,
  "booking_revenue_last_year": 0.0,
  "direct_revenue_last_month": 0.0,
  "direct_revenue_last_year": 0.0
}
```

# Top desitination

## `/airline-staff/misc/top-destination`

**Request**: `GET`

>http://localhost:5000/api/airline-staff/misc/top-destination

Find the top destination in the airline the staff works for in last 3 month and last year.

Request Parameters Query Parameters

Input Type: Static Values

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- |
| limit | int | The top number to display | No | Defalted to be 3 |

**Json Response**

Root object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| top_month_destination | array | Top destination last 3 month | |
| top_year_destination | array | Top destination last year | |

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/top-destination?limit=5"
```

Response

```json
{
  "top_month_destination": [],
  "top_year_destination": []
}
```

# Grant new permission

## `/airline-staff/misc/grant-permission`

>http://localhost:5000/api/airline-staff/misc/grant-permission

**Request**: `POST`

Airline staff who has the "Admin" permission, can grant new permission for other staff works for the same airline.

**Request Parameters**

**Input Type**: `application/json`

Root object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| airline_staff_username | string | the username of the airline staff who need the new permission | yes | |
| permission | string | the granted permission | yes | it can only be in ["Admin", "Operator"]


**Json response**:
Root Object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | the permission granted successfully or not | |

**Example**

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/grant-permission" -d "{\"airline_staff_username\": \"operatorStaff1\", \"permission\": \"Admin\"}"
```

Response

```json
{
  "status": "success"
}
```