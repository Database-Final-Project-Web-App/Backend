from flask import Blueprint, jsonify, request, current_app, session
from app.utils.db import KV_ARG, find_airline_for_staff, find_permission, V_ARG
from app.utils.auth import is_logged_in, LOGINTYPE, PERMISSION

airplane_bp = Blueprint('airplane', __name__, url_prefix='/airplane')

@airplane_bp.route('/add', methods=["POST"])
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
		return jsonify({"error": "You don't have the permission to add airplane."}), 400
	airline_name = find_airline_for_staff(db, username)
	data = request.get_json()
	seat_num = data.get("seat_num", None)

	#add airplane
	create_airplane_query_template = \
	"""
	INSERT INTO airplane(airline_name, seat_num)
	VALUES ({airline_name}, {seat_num})
	"""

	create_airplane_query = create_airplane_query_template.format(
		airline_name=V_ARG("string", airline_name),
		seat_num=V_ARG("number", seat_num)
	)

	create_airplane_result = db.execute_query(create_airplane_query)
	if create_airplane_result is None:
		return jsonify({"error": "Internal error"}), 500
	
	db.commit()
	return jsonify({"status": "success"}), 200