from flask import Blueprint, jsonify, request, current_app

from app.utils.db import ARG


flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/search', methods=["POST"])
def search_handler():
	# define query template
	query_template = \
	"""
	SELECT *
	FROM flight
	WHERE {flight_num}
	AND {airline_name}
	AND {arrival_time}
	AND {departure_time}
	AND {price}
	AND {status}
	AND {airplane_id}
	AND {arr_airport_name}
	AND {dep_airport_name}
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
	dep_airport_name = data.get("dep_airport_name", None)

	# build query
	query = query_template.format(
		flight_num=ARG("flight_num", "number", flight_num),
		airline_name=ARG("airline_name", "string", airline_name),
		arrival_time=ARG("arrival_time", "string", arrival_time),
		departure_time=ARG("departure_time", "string", departure_time),
		price=ARG("price", "number", price),
		status=ARG("status", "string", status),
		airplane_id=ARG("airplane_id", "number", airplane_id),
		arr_airport_name=ARG("arr_airport_name", "string", arr_airport_name),
		dep_airport_name=ARG("dep_airport_name", "string", dep_airport_name)
	)

	# execute query (get `db` from app config)
	db = current_app.config['db']
	query_result = db.execute_query(query)

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
			"dep_airport_name": row[8]
		})	

	# return result as json	
	return jsonify({"flights": result}), 200 
	