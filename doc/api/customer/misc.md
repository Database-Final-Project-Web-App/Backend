# Customer tracking spending

## `/customer/misc/spending`

>http://localhost:5000/api/customer/misc/spending

**Request**: `GET`

Tracking the monthly spending and also the total spending in a range of time.

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
| start_date | string | The beginning of the time range | format: `YYYY-MM-DD HH:MM` |
| end_date | string | The end of the time range | format: `YYYY-MM-DD HH:MM`, defaulted current date |
| monthly_spending | dictionary | Monthly spending | |
| total_spending | float | Total spending | |

`monthly_spending[i]` object:

| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| year-name | float | monthly spending |

**Example**

Request

```bash
curl -X GET -b cookie.txt -c cookie.txt "http://localhost:5000/api/customer/misc/spending?start_date=2023-01-01&end_date=2024-01-01"
```

response

```json
{
  "end_date": "2024-01-01",
  "monthly_spending": {
    "2023-11": 150.0,
    "2023-12": 1405.0
  },
  "start_date": "2023-01-01",
  "total_spending": 1555.0
}
```