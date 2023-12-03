**Example**

Request

$ curl -X POST -b cookie.txt -c cookie.txt "http://localhost:5000/api/customer/ticket/purchase" -H "Content-Type: application/json" -d "{\"flight_num\": 1, \"airline_name\": \"Air Canada\"}"