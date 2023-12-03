from flask import Blueprint, jsonify, request, current_app, session
from app.utils.db import KV_ARG, find_permission, V_ARG
from app.utils.auth import is_logged_in, LOGINTYPE, PERMISSION

airport_bp = Blueprint('airport', __name__, url_prefix='/airport')

@airport_bp.route('/add', methods=["POST"])
def add_handler():
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	permission = find_permission(db, username)
	if PERMISSION.ADMIN not in permission:
		return jsonify({"error": "You don't have the permission to add airport."}), 400
	data = request.get_json()
	airport_name = data.get("name", None)
	city = data.get("city", None)

	if airport_name is None or city is None:
		return jsonify({"error": "name and city are required."}), 400

	# check if the airport already exist
	check_airport_query_template = \
	"""
	SELECT * FROM airport
	WHERE {airport_name}
	"""
	
	check_airport_query = check_airport_query_template.format(
		airport_name=KV_ARG("name", "string", airport_name)
	)

	check_airport_result = db.execute_query(check_airport_query)
	if check_airport_result is None:
		return jsonify({"error": "Internal error"}), 500
	
	if len(check_airport_result) != 0:
		return jsonify({"error": "Airport already exist."}), 400
	
	#add airport
	create_airport_query_template = \
	"""
	INSERT INTO airport
	VALUES ({airport_name}, {city})
	"""

	create_airport_query = create_airport_query_template.format(
		airport_name=V_ARG("string", airport_name),
		city=V_ARG("string", city)
	)

	create_airport_result = db.execute_query(create_airport_query)
	if create_airport_result is None:
		return jsonify({"error": "Query failed."}), 500
	
	db.commit()
	return jsonify({"status": "success"}), 200