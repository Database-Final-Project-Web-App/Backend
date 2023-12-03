
# Login

## `/auth/login`

> http://localhost:5000/api/auth/login

**Request**: `Post`

Search for users with given parameters, if the user exists, create the session

**Request Parameters**

**Input Type**: form

Root Object:

| Name | Type | Description | required? | note |
| ---- | ---- | ----------- | --------- | ---- | 
| logintype | string | User's type | yes | |
| username | string | username | yes | |
| password | string | password | yes | |

**json responce**

Root Objects:
| Name | Type | Description | note |
| ---- | ---- | ----------- | ---- |
| status | string | login successful or not | |
| message | string | the error message or successful message | |

**Example**:

Request

```bash
curl -X POST -H "Content-Type: application/json" -b cookie.txt -c cookie.txt -d "{\"username\":\"customer1@example.com\", \"password\":\"password1\", \"logintype\":\"customer\"}" http://localhost:5000/api/auth/login
```

Response

```json
{
  "message": "Successfully logged in",
  "status": "success",

}
```
