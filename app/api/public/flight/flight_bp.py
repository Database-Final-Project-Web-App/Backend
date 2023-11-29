from flask import Blueprint, jsonify, request, current_app

from app.utils.db import KV_ARG, search_flight


flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/search', methods=["POST"])
def search_handler():
	# get parameters from json request
	data = request.get_json()
	flight_id = data.get("flight_id", None)
	airline_name = data.get("airline_name", None)
	arrival_time = data.get("arrival_time", None)
	departure_time = data.get("departure_time", None)
	price = data.get("price", None)
	status = data.get("status", "upcoming")
	airplane_id= data.get("airplane_id", None)
	arr_airport_name = data.get("arr_airport_name", None)
	dept_airport_name = data.get("dept_airport_name", None)
	arr_city = data.get("arr_city", None)
	dept_city = data.get("dept_city", None)

	query_result = search_flight(
		flight_id=flight_id,
		airline_name=airline_name,
		arrival_time=arrival_time,
		departure_time=departure_time,
		price=price,
		status=status,
		airplane_id=airplane_id,
		arr_airport_name=arr_airport_name,
		dept_airport_name=dept_airport_name,
		arr_city=arr_city,
		dept_city=dept_city
	)

	if query_result is None:
		return jsonify({
			"error": "Invalid query"
		}), 400
	# process query result
	result = []
	for row in query_result:
		result.append({
			"flight_id": row[0],
			"airline_name": row[1],
			"departure_time": row[2],
			"arrival_time": row[3],
			"price": row[4],
			"status": row[5],
			"airplane_id": row[6],
			"arr_airport_name": row[7],
			"dept_airport_name": row[8],
			"dept_city": row[9],
			"arr_city": row[10]
		})	

	if len(result) == 0:
		return jsonify({"error": "No results found"}), 404

	# return result as json	
	return jsonify({"flights": result}), 200 
	