from flask import Blueprint, jsonify, request, current_app

from app.utils.db import KV_ARG, date2datetime_range


flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/search', methods=["POST"])
def search_handler():
	# define query template
	query_template = \
	"""
	WITH flight_city AS
	(SELECT flight.*, a1.city AS dept_city, a2.city AS arr_city
	FROM airport AS a1, airport AS a2, flight
	WHERE a1.name = flight.dept_airport_name 
	AND a2.name = flight.arr_airport_name)
	SELECT *
	FROM flight_city
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
	"""

	# get parameters from json request
	data = request.get_json()
	flight_num = data.get("flight_num", None)
	airline_name = data.get("airline_name", None)
	departure_date = data.get("departure_date", None)
	arrival_date = data.get("arrival_date", None)
	price = data.get("price", None)
	status = data.get("status", None)
	airplane_id= data.get("airplane_id", None)
	dept_airport_name = data.get("dept_airport_name", None)
	arr_airport_name = data.get("arr_airport_name", None)
	dept_city = data.get("dept_city", None)
	arr_city = data.get("arr_city", None)

	departure_time = date2datetime_range(departure_date)
	arrival_time = date2datetime_range(arrival_date)

	# build query
	query = query_template.format(
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
		dept_city=KV_ARG("dept_city", "string", dept_city)
	)

	# execute query (get `db` from app config)
	db = current_app.config['db']
	query_result = db.execute_query(query, cursor_type="dict")
	# breakpoint()
	if query_result is None:
		return jsonify({
			"error": "Invalid query"
		}), 400
	# process query result
	result = []
	for row in query_result:
		result.append(
			{key: value for key, value in row.items() if value is not None}
		)
		# result.append({
		# 	"flight_num": row[0],
		# 	"airline_name": row[1],
		# 	"departure_time": row[2],
		# 	"arrival_time": row[3],
		# 	"price": row[4],
		# 	"status": row[5],
		# 	"airplane_id": row[6],
		# 	"arr_airport_name": row[7],
		# 	"dept_airport_name": row[8],
		# 	"dept_city": row[9],
		# 	"arr_city": row[10]
		# })	

	# breakpoint()
	if result is None:
		return jsonify({
			"error": "Internal error"
		}), 500 
	# breakpoint()
	# return result as json	
	return jsonify({"flights": result}), 200 
	