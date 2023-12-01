from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime

from app.utils.db import KV_ARG, find_airline, find_permission
from app.utils.auth import is_logged_in, LOGINTYPE, PERMISSION

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/my', methods=["POST"])
def my_handler():
	# defalt will be all upcoming flights operated by the airline the airline staff works for in the next 30 days
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]

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
	WHERE {flight_num}
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
	airline_name = find_airline(db, username)
	departure_time = data.get("departure_time", None)
	arrival_time = data.get("arrival_time", None)
	price = data.get("price", None)
	status = data.get("status", None)
	airplane_id = data.get("airplane_id", None)
	arr_airport_name = data.get("arr_airport_name", None)
	dept_airport_name = data.get("dept_airport_name", None)
	arr_city = data.get("arr_city", None)
	dept_city = data.get("dept_city", None)
	ticket_id = data.get("ticket_id", None)
	start_date = data.get("start_date", None)
	end_date = data.get("end_date", None)

	# build query
	search_query = search_query_template.format(
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
		ticket_id=KV_ARG("ticket_id", "number", ticket_id),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)

	# execute query
	search_result = db.execute_query(search_query)

	if search_result is None:
		return jsonify({"error": "Query failed"}), 500

	# return result
	result = []
	for row in search_result:
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
	return jsonify({"flights": result}), 200

@flight_bp.route('/create', methods=["POST"])
def create_handler():
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	db = current_app.config["db"]
	# make sure the user has the right to create flight
	if logintype != 'airline_staff':
		return jsonify({"error": "you must login as airline staff"}), 400
	else:
		permission = find_permission(db, username)
		if PERMISSION.ADMIN not in permission:
			return jsonify({"error": "you don't have the permission to create flight"}), 400
	
	# get parameters from json request
	data = request.get_json()
	airline_name = find_airline(db, username)
	departure_time = data.get("departure_time", None)
	arrival_time = data.get("arrival_time", None)
	price = data.get("price", None)
	status = data.get("status", None)
	airplane_id = data.get("airplane_id", None)
	arr_airport_name = data.get("arr_airport_name", None)
	dept_airport_name = data.get("dept_airport_name", None)

	# build query
	create_query_template = \
	"""
	INSERT INTO flight
	VALUES ({airline_name},
		{departure_time},
		{arrival_time},
		{price},
		{status},
		{airplane_id},
		{arr_airport_name},
		{dept_airport_name})
	"""

	create_query = create_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		arrival_time=KV_ARG("arrival_time", "datetime", arrival_time),
		departure_time=KV_ARG("departure_time", "datetime", departure_time),
		price=KV_ARG("price", "number", price),
		status=KV_ARG("status", "string", status),
		airplane_id=KV_ARG("airplane_id", "number", airplane_id),
		arr_airport_name=KV_ARG("arr_airport_name", "string", arr_airport_name),
		dept_airport_name=KV_ARG("dept_airport_name", "string", dept_airport_name)
	)

	# execute query
	create_result = db.execute_query(create_query)
	if create_result is None:
		return jsonify({"error": "Query failed"}), 500
	return jsonify({"status": "success"}), 200

@flight_bp.route('/change-status', methods=["POST"])
def change_status_handler():
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	db = current_app.config["db"]
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	else:
		permission = find_permission(db, username)
		if PERMISSION.OPERATOR not in permission:
			return jsonify({"error": "you don't have the permission to change flight status"}), 400
		
	# get parameters from json request
	data = request.get_json()
	airline_name = find_airline(db, username)
	flight_num = data.get("flight_num", None)
	status = data.get("status", None)

	# build query
	change_status_query_template = \
	"""
	UPDATE flight
	SET status = {status}
	WHERE airline_name = {airline_name}
	AND flight_num = {flight_num}
	"""

	change_status_query = change_status_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		flight_num=KV_ARG("flight_num", "number", flight_num),
		status=KV_ARG("status", "string", status)
	)

	# execute query
	change_status_result = db.execute_query(change_status_query)
	if change_status_result is None:
		return jsonify({"error": "Query failed"}), 500
	return jsonify({"status": "success"}), 200

