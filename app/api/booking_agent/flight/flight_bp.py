from flask import Blueprint, request, jsonify, session, current_app

from app.utils.db import KV_ARG
from app.utils.auth import is_logged_in, LOGINTYPE

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/my', methods=['POST'])
def my_handler():
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.BOOKING_AGENT:
		return jsonify({"error": "You must login as booking agent."}), 400

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
	WHERE {customer_email}
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
	AND {booking_agent_email}
	AND {ticket_id}
	AND {purchase_date}
	"""

	# get parameters from json request
	data = request.get_json()
	customer_email = data.get("customer_email", None)
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
		customer_email=KV_ARG("customer_email", "string", customer_email),
		flight_num=KV_ARG("flight_id", "number", flight_num),
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
		booking_agent_email=KV_ARG("booking_agent_email", "string", username),
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
				"departure_time": row[2],
				"arrival_time": row[3],
				"price": row[4],
				"status": row[5],
				"airplane_id": row[6],
				"arr_airport_name": row[7],
				"dept_airport_name": row[8],
				"dept_city": row[9],
				"arr_city": row[10],
				"ticket_id": row[11],
				"customer_email": row[12],
				"booking_agent_email": row[13],
				"purchase_date": row[14],
			})

	if result is None:
		return jsonify({"error": "Query failed"}), 500

	return jsonify({"flights": result}), 200
