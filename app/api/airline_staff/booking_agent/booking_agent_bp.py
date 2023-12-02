from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime, timedelta
from app.utils.db import KV_ARG, find_airline_for_staff, find_permission
from app.utils.auth import is_logged_in, LOGINTYPE, PERMISSION

booking_agent_bp = Blueprint('booking_agent', __name__, url_prefix='/booking-agent')

@booking_agent_bp.route('/all', methods=["GET"])
def all_handler():
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	current_date = datetime.now().strftime("%Y-%m-%d")
	one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
	one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
	
	# Top 5 booking agents works for the airline in terms of number of tickets sold for the past month, and last year
	top_tickets_query_template = \
	"""
	SELECT booking_agent_id, COUNT(ticket_id) AS num_tickets
	FROM ticket 
	WHERE {airline_name}
	AND {purchase_date}
	GROUP BY booking_agent_id
	ORDER BY num_tickets DESC
	LIMIT {limit}
	"""

	data = request.get_json()
	limit = data.get("limit", None)

	top_tickets_month_query = top_tickets_query_template.format(
		airline_name=find_airline_for_staff(db, username),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_month_ago, current_date)),
		limit=limit
	)

	top_ticket_year_query = top_tickets_query_template.format(
		airline_name=find_airline_for_staff(db, username),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date)),
		limit=limit
	)

	top_tickets_month_result = db.execute_query(top_tickets_month_query)
	top_tickets_year_result = db.execute_query(top_ticket_year_query)

	if top_tickets_month_result is None or top_tickets_year_result is None:
		return jsonify({"error": "Query failed."}), 500
	
	# Top 5 booking agents works for the airline in terms of commission received for last year
	top_commission_query_template = \
	"""
	SELECT booking_agent_id, SUM(price * 0.1) AS commission
	FROM ticket
	WHERE {airline_name}
	AND {purchase_date}
	GROUP BY booking_agent_id
	ORDER BY commission DESC
	LIMIT {limit}
	"""

	top_commission_year_query = top_commission_query_template.format(
		airline_name=find_airline_for_staff(db, username),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date)),
		limit=limit
	)

	top_commission_year_result = db.execute_query(top_commission_year_query)

	if top_commission_year_result is None:
		return jsonify({"error": "Query failed."}), 500
	return jsonify({
		"Top 5 booking agent based on the number of tickets for last month": top_tickets_month_result,
		"Top 5 booking agent based on the number of tickets for last year": top_tickets_year_result,
		"Top 5 booking agent based on the commission received for last year": top_commission_year_result
	}), 200

@booking_agent_bp.route('/add', methods=["POST"])
def add_handler():
	"""
	check whether the user is logged in
	check logintype
	check permission
	check whether the booking agent works for the airline
	"""
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
		return jsonify({"error": "You don't have the permission to add booking agent."}), 400
	data = request.get_json()
	airline_name = find_airline_for_staff(db, username)
	booking_agent_email = data.get("booking_agent_email", None)
	
	# check whether the booking agent works for the airline
	check_query_template = \
	"""
	SELECT booking_agent_email
	FROM booking_agent_works_for
	WHERE {booking_agent_email}
	AND {airline_name}
	"""
	check_query = check_query_template.format(
		booking_agent_email=KV_ARG("booking_agent_email", "string", booking_agent_email),
		airline_name=KV_ARG("airline_name", "string", airline_name)
	)
	check_result = db.execute_query(check_query)
	if check_result is None:
		return jsonify({"error": "Query failed."}), 500
	if len(check_result) != 0:
		return jsonify({"error": "The booking agent already works for the airline."}), 400
	
	# add booking agent
	add_query_template = \
	"""
	INSERT INTO booking_agent_works_for
	VALUES ({booking_agent_email}, {airline_name})
	"""
	add_query = add_query_template.format(
		booking_agent_email=KV_ARG("booking_agent_email", "string", booking_agent_email),
		airline_name=KV_ARG("airline_name", "string", airline_name)
	)
	add_result = db.execute_query(add_query)
	if add_result is None:
		return jsonify({"error": "Query failed."}), 500
	
	return jsonify({"status": "success"}), 200