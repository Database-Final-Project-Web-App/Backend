from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime, timedelta
from app.utils.db import KV_ARG, find_airline_for_staff, find_permission, V_ARG
from app.utils.auth import is_logged_in, LOGINTYPE, PERMISSION
from app.utils.misc import COMMISSION_RATE

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')


@misc_bp.route('/frequent-customer', methods=["GET"])
def frequent_customer_handler():
	"""
	Top customers in terms of number of tickets purchased from the airline in last year
	"""
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	current_date = datetime.now().strftime("%Y-%m-%d")
	one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
	
	# Top 5 customers in terms of number of tickets purchased from the airline in last year
	top_tickets_query_template = \
	"""
	SELECT customer_email, COUNT(ticket_id) AS num_tickets
	FROM ticket 
	WHERE {airline_name}
	AND {purchase_date}
	GROUP BY customer_email
	ORDER BY num_tickets DESC
	LIMIT {limit}
	"""

	limit = request.args.get("limit", None)
	airline_name = find_airline_for_staff(db, username)

	top_tickets_year_query = top_tickets_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date)),
		limit=limit
	)

	top_tickets_year = db.execute_query(top_tickets_year_query)

	if top_tickets_year is None:
		return jsonify({"error": "Internal server error."}), 500
	
	if len(top_tickets_year) == 0:
		return jsonify({"error": "No customer found."}), 400
	
	# See the list of flights that the customer has taken in the past year
	search_flights_query_template = \
	"""
	SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name)
	WHERE {customer_email}
	AND {airline_name}
	AND {purchase_date}
	"""
	
	flights = []
	for customer in top_tickets_year:
		customer_email = customer[0]
		search_flights_query = search_flights_query_template.format(
			customer_email=KV_ARG("customer_email", "string", customer_email),
			airline_name=KV_ARG("airline_name", "string", airline_name),
			purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date)),
		)
		flights_result = db.execute_query(search_flights_query)
		if flights_result is None:
			return jsonify({"error": "Internal server error."}), 500
		flights.append({customer_email: flights_result})
		
	return jsonify({"top_frequent_customers": top_tickets_year, "flights": flights}), 200


@misc_bp.route('/report', methods=["GET"])
def report_handler():
	"""
	Total amount of ticket sales for the past month, and last year, range of dates specified by the user
	Monthly report of tickets
	"""
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	start_date = request.args.get("start_date", None)
	end_date = request.args.get("end_date", None)
	airline_name = find_airline_for_staff(db, username)

	# Total amount of ticket sales for the past month
	report_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price) AS total_amount, count(ticket_id) AS num_tickets
	FROM my_ticket
	WHERE {airline_name}
	AND {purchase_date}
	"""

	report_query = report_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)

	report = db.execute_query(report_query)

	if report is None:
		return jsonify({"error": "Query failed."}), 500
	
	report = {"Total amount": float(report[0][0]), "Number of tickets sold": float(report[0][1])}if report[0][0] else (0.0, 0.0)
	
	# Monthly report of tickets
	monthly_report_tickets_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT COUNT(ticket_id) AS num_tickets, YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, SUM(price) AS monthly_amount
	FROM my_ticket
	WHERE {airline_name}
	AND {purchase_date}
	GROUP BY year, month
	"""

	monthly_report_tickets_query = monthly_report_tickets_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)

	monthly_report_tickets = db.execute_query(monthly_report_tickets_query)

	if monthly_report_tickets is None:
		return jsonify({"error":"Internal server error."}), 500
	
	m = {}
	for row in monthly_report_tickets:
		# format to YYYY-MM
		m["{}-{:02}".format(row[1], row[2])] = {"number of tickets": float(row[0]), "Total amount":float(row[3])} if row[0] else (0.0, 0.0)
	monthly_report_tickets = m
	
	return jsonify({
		"start_date": start_date,
		"end_date": end_date,
		"Total amount of tickets": report,
		"Monthly_report_tickets": monthly_report_tickets
	}), 200


@misc_bp.route('/revenue-comparison', methods=["GET"])
def revenue_comparison_handler():
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	current_date = datetime.now().strftime("%Y-%m-%d")
	one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
	one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
	airline_name = find_airline_for_staff(db, username)

	# Total amount of ticket sales for the past month from direct sales
	direct_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price) AS total_amount
	FROM my_ticket
	WHERE {airline_name}
	AND {purchase_date}
	AND {booking_agent_email}
	"""

	direct_month_query = direct_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_month_ago, current_date)),
		booking_agent_email=KV_ARG("booking_agent_email", "string", None)
	)

	direct_month = db.execute_query(direct_month_query)

	if direct_month is None:
		return jsonify({"error": "Internal server error."}), 500
	
	direct_month = float(direct_month[0][0]) if direct_month[0][0] else 0.0

	# Total amount of ticket sales for the past month from booking agent
	booking_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price) AS total_amount
	FROM my_ticket
	WHERE {airline_name}
	AND {purchase_date}
	AND booking_agent_email IS NOT NULL
	"""

	booking_month_query = booking_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_month_ago, current_date))
	)

	booking_month = db.execute_query(booking_month_query)

	if booking_month is None:
		return jsonify({"error": "Internal server error."}), 500
	
	booking_month = float(booking_month[0][0]) if booking_month[0][0] else 0.0

	# Total amount of ticket sales for the past year from direct sales
	direct_year_query = direct_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date)),
		booking_agent_email=KV_ARG("booking_agent_email", "string", None)
	)

	direct_year = db.execute_query(direct_year_query)
	
	if direct_year is None:
		return jsonify({"error": "Internal server error."}), 500
	
	direct_year = float(direct_year[0][0]) if direct_year[0][0] else 0.0

	# Total amount of ticket sales for the past year from booking agent
	booking_year_query = booking_query_template.format(
		airline_name=KV_ARG("airline_name", "string", airline_name),
		purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date))
	)

	booking_year = db.execute_query(booking_year_query)

	if booking_year is None:
		return jsonify({"error": "Internal server error."}), 500
	
	booking_year = float(booking_year[0][0]) if booking_year[0][0] else 0.0

	return jsonify({
		"direct_revenue_last_month": direct_month,
		"booking_revenue_last_month": booking_month,
		"direct_revenue_last_year": direct_year,
		"booking_revenue_last_year": booking_year
	}), 200


@misc_bp.route('/top-destination', methods=["GET"])
def top_destination_handler():
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	current_date = datetime.now().strftime("%Y-%m-%d")
	three_month_ago = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
	one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
	airline_name = find_airline_for_staff(db, username)
	limit = request.args.get("limit", None)

	# Top 3 destination in terms of number of tickets sold in the past 3 months
	top_tickets_query_template = \
	"""
	WITH flight_city AS
	(SELECT flight.*, a1.city AS dept_city, a2.name AS arr_city
	FROM airport AS a1, airport AS a2, flight
	WHERE a1.name = flight.dept_airport_name 
	AND a2.name = flight.arr_airport_name)
	SELECT arr_city, COUNT(ticket_id) AS num_tickets
	FROM flight_city NATURAL JOIN ticket
	WHERE {purchase_date}
	AND {airline_name}
	GROUP BY arr_city
	ORDER BY num_tickets DESC
	LIMIT {limit}
	"""

	top_month_tickets_query = top_tickets_query_template.format(
		purchase_date=KV_ARG("purchase_date", "datetime", (three_month_ago, current_date)),
		airline_name=KV_ARG("airline_name", "string", airline_name),
		limit=limit
	)

	top_month_tickets = db.execute_query(top_month_tickets_query)

	if top_month_tickets is None:
		return jsonify({"error": "Internal server error."}), 500
	
	top_year_tickets_query = top_tickets_query_template.format(
		purchase_date=KV_ARG("purchase_date", "datetime", (one_year_ago, current_date)),
		airline_name=KV_ARG("airline_name", "string", airline_name),
		limit=limit
	)

	top_year_tickets = db.execute_query(top_year_tickets_query)

	if top_year_tickets is None:
		return jsonify({"error": "Internal server error."}), 500
	
	return jsonify({
		"top_month_destination": top_month_tickets,
		"top_year_destination": top_year_tickets
	}), 200


@misc_bp.route('/grant-permission', methods=["POST"])
def grant_permission_handler():
	"""
	Grant new permission for another airline staff working for the same airline
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
		return jsonify({"error": "You must be admin to grant permission."}), 400
	data = request.get_json()
	airline_name = find_airline_for_staff(db, username)
	grant_username = data.get("airline_staff_username", None)
	grant_permission = data.get("permission", None)
	if grant_permission not in [PERMISSION.ADMIN, PERMISSION.OPERATOR, PERMISSION.NORMAL]:
		return jsonify({"error": "Invalid permission."}), 400
	
	# check if the user is working for the same airline
	working_airline = find_airline_for_staff(db, grant_username)

	if working_airline != airline_name:
		return jsonify({"error": "The staff is not working for the same airline."}), 400
	
	# check if the user already has the permission
	permission_for_staff = find_permission(db, grant_username)
	if grant_permission in permission_for_staff:
		return jsonify({"error": "The staff already has the permission."}), 400
	
	# grant permission
	grant_query_template = \
	"""
	INSERT INTO airline_staff_permission
	VALUES ({username}, {permission})
	"""

	grant_query = grant_query_template.format(
		username=V_ARG("string", grant_username),
		permission=V_ARG("string", grant_permission)
	)

	grant_result = db.execute_query(grant_query)

	if grant_result is None:
		return jsonify({"error": "Internal server error."}), 500
	
	db.commit()
	return jsonify({"status": "success"}), 200