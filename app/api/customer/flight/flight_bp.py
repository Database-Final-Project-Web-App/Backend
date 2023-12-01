from flask import Blueprint, jsonify, request, current_app, session

from app.utils.db import KV_ARG

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/my', methods=["POST"])
def my_handler():
	# get username from session
	username = session['user']['username']

	# define query template
	search_query_template = \
	"""
	WITH flight_city AS
	(SELECT flight.*, a1.city AS dept_city, a2.name AS arr_city
	FROM airport AS a1, airport AS a2, flight
	WHERE a1.name = flight.dept_airport_name 
	AND a2.name = flight.arr_airport_name)
	SELECT * 
	FROM flight_city NATURAL JOIN ticket
	WHERE {username}
	AND {flight_num}
	AND {airline_name}
	AND {arrival_time}
	AND {departure_time}
	AND {price}
	AND {status}
	AND {airplane_id}
	AND {arr_airport_name}
	AND {dept_airport_name}
	AND {arr_city}
	AND {dept_city}
	AND {ticket_id}
	AND {purchase_date}
	"""

	# get parameters from json request
	data = request.get_json()
	flight_num = data.get("flight_num", None)
	airline_name = data.get("airline_name", None)
	arrival_time = data.get("arrival_time", None)
	departure_time = data.get("departure_time", None)
	price = data.get("price", None)
	status = data.get("status", None)
	airplane_id= data.get("airplane_id", None)
	arr_airport_name = data.get("arr_airport_name", None)
	dept_airport_name = data.get("dept_airport_name", None)
	arr_city = data.get("arr_city", None)
	dept_city = data.get("dept_city", None)
	ticket_id = data.get("ticket_id", None)
	purchase_date = data.get("purchase_date", None)

	# build query
	search_query = search_query_template.format(
		username=KV_ARG("customer_email", "string", username),
		flight_num=KV_ARG("flight_num", "number", flight_num),
		airline_name=KV_ARG("airline_name", "string", airline_name),
		arrival_time=KV_ARG("arrival_time", "datetime", arrival_time),
		departure_time=KV_ARG("departure_time", "datetime", departure_time),
		price=KV_ARG("price", "number", price),
		status=KV_ARG("status", "string", status),
		airplane_id=KV_ARG("airplane_id", "number", airplane_id),
		arr_airport_name=KV_ARG("arr_airport_name", "string", arr_airport_name),
		dept_airport_name=KV_ARG("dept_airport_name", "string", dept_airport_name),
		arr_city=KV_ARG("arr_city", "string", arr_city),
		dept_city=KV_ARG("dept_city", "string", dept_city),
		ticket_id=KV_ARG("ticket_id", "string", ticket_id),
		purchase_date=KV_ARG("purchase_datetime", "datetime", purchase_date)
	)

	# execute query from app config
	db = current_app.config["db"]
	query_result = db.execute_query(search_query)

	if query_result is None:
		return jsonify({"error": "Query failed"}), 500
	
	# process query result
	result = []
	for row in query_result:
		result.append({
			"flight_num": row[0],
			"airline_name": row[1],
			"arrival_time": row[2],
			"departure_time": row[3],
			"price": row[4],
			"status": row[5],
			"airplane_id": row[6],
			"arr_airport_name": row[7],
			"dept_airport_name": row[8],
			"arr_city": row[9],
			"dept_city": row[10],
			"ticket_id": row[11],
			"purchase_date": row[12]
		})

	if result is None:
		return jsonify({"error": "Query failed"}), 500

	return jsonify({"flights": result}), 200