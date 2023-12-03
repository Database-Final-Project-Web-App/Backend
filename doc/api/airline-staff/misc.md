# Top frequent customer

## `/airline-staff/misc/frequent-customer`

Method: `GET`

**Example**

Request

```bash
curl -X GET -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/frequent-customer?limit=5"
```

Response

```json
{
  "top_frequent_customers": []
}
```

# View report

## `/airline-staff/misc/report`

Method: `GET`

**Example**

Request

```bash
curl -X GET -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/report?start_date=2023-06-01&end_date=2024-06-01"
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

Method: `GET`

**Example**

Request

```bash
curl -X GET -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/revenue-comparison"
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

Method: `GET`

**Example**

Request

```bash
curl -X GET -H "Content-Type: application/json" -b cookie.txt -c cookie.txt "http://localhost:5000/api/airline-staff/misc/top-destination?limit=5"
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

Method: `POS`

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