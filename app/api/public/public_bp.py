from flask import Blueprint, current_app, session, jsonify, request

from .flight.flight_bp import flight_bp

from app.utils.db import KV_ARG, V_ARG
from app.utils.auth import LOGINTYPE, is_logged_in

public_bp = Blueprint('public', __name__, url_prefix='/public')

# register blueprints
public_bp.register_blueprint(flight_bp, url_prefix=flight_bp.url_prefix)

# get customer info
@public_bp.route('/whoami', methods=["GET"])
def whoami_handler():
	db = current_app.config["db"]
	if not is_logged_in():
		return jsonify({
			"status": 'error',
			"message": 'You must be logged in to access this information.'
		}), 401
	
	username = session['user']['username']
	query_template = \
	"""
	SELECT {columnname} 
	FROM {tablename}
	WHERE {username}
	"""
	
	column_name = {
		LOGINTYPE.CUSTOMER: ["email", "name", "building_number", "street", "city", "state", "phone_number", "passport_number", "passport_expiration", "passport_country", "date_of_birth"],
		LOGINTYPE.BOOKING_AGENT: ["email", "booking_agent_id", "airline_name"],
		LOGINTYPE.AIRLINE_STAFF: ["username", "first_name", "last_name", "date_of_birth", "airline_name", "permission"]
	}[session['user']['logintype']]
	table_name = {
		LOGINTYPE.CUSTOMER: "customer",
		LOGINTYPE.BOOKING_AGENT: "booking_agent NATURAL JOIN booking_agent_workfor",
		LOGINTYPE.AIRLINE_STAFF: "airline_staff LEFT JOIN airline_staff_permission USING (username)"
	}[session['user']['logintype']]
	id_attr_name = {
		LOGINTYPE.CUSTOMER: "email",
		LOGINTYPE.BOOKING_AGENT: "email",
		LOGINTYPE.AIRLINE_STAFF: "username"
	}[session['user']['logintype']]

	query = query_template.format(
		columnname=", ".join(column_name),
		tablename=table_name,
		username=KV_ARG(id_attr_name, "string", username)
	)
	query_result = db.execute_query(query, cursor_type='dict')
	if not query_result:
		return jsonify({
			"status": 'error',
			"message": 'Query failed.'
		}), 500
	if len(query_result) == 0:
		return jsonify({
			"status": 'error',
			"message": 'User does not exist.'
		}), 401
	# breakpoint()	
	
	# special data post-processing
	# create a list of permission for airline staff from the query result
	# breakpoint()

	result = {
		"status": 'success',
		"message": 'User info retrieved successfully.',
		"data": None
	}

	if session['user']['logintype'] != LOGINTYPE.AIRLINE_STAFF:
		result['data'] = query_result[0]
		return jsonify(result), 200
	
	perms = []
	for row in query_result:
		perms.append(row['permission'])
	result['data'] = query_result[0]
	result['data']['permission'] = perms
	
	return jsonify(result), 200

