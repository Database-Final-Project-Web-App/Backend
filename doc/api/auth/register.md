# Register

## `/auth/register`

> http://localhost:5000/api/auth/register

**Request**: `Post`

Search for users with given parameters, if the user didn't exist, then insert the value into the form.

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
| status | string | registration successful or not | |
| message | string | the error message or successful message | |

**Example**:

Request

```python
def test_auth():
    # register a new user
    url = "http://localhost:5000/api/auth/register"
    data = {
        "username": "customer3@example.com",
        "password": "password",
        "logintype": "customer",
        "building_number": "123",
        "street": "streetA",
    }

    # send POST request with form data
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.text)
```

Response

```json
200
{
  "message": "Successfully registered",
  "status": "success"
}
```

