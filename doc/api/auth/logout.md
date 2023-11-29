
# Logout

## `/auth/logout`

> http://localhost:5000/api/auth/logout

**Request**: `Post`

pop the user from the session

**Request Parameters**

**Input Type**: form

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| user | array | contains username and the type | yes | |

**json responce**

Root Objects:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | loggout successful or not | |
| message | string | the error message or successful message | |

**Example**:

Request

```bash
curl -X POST localhost:5000/api/auth/logout -b cookie.txt -c cookie.txt
```

Response

```json
{
  "message": "Successfully logged out",
  "status": "success"
}
```
