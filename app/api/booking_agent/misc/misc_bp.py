from flask import Blueprint, jsonify, request, current_app, session

from app.utils.db import KV_ARG
from app.utils.auth import is_logged_in, LOGINTYPE

from app.utils.misc import COMMISSION_RATE

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')

@misc_bp.route('/commission', methods=['GET'])
def commission_handler():
	# get booking agent username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.BOOKING_AGENT:
		return jsonify({"error": "You must login as booking agent."}), 400
	# current_date = date.today().strftime("%Y-%m-%d")
	# default_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")

	if username is None:
		return jsonify({"error": "you must login first"}), 400

	# get parameters from url
	start_date = request.args.get("start_date", None)
	end_date = request.args.get("end_date", None)

	# search for flight within a specific time period, default to 30 days
	# get the total commission, number of tickets sold, and average commission per ticket
	commission_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price * {COMMISSION_RATE}) AS commission, COUNT(*) AS num_tickets, AVG(price * {COMMISSION_RATE}) AS avg_commission
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	"""

	commission_query = commission_query_template.format(
		COMMISSION_RATE=COMMISSION_RATE,
		username=KV_ARG("booking_agent_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)
	# breakpoint()
	db = current_app.config["db"]
	commission_result = db.execute_query(commission_query, cursor_type="dict")
	if commission_result is None:
		return jsonify({"error": "Internal error"}), 500
	commission = commission_result[0]
	if (commission["num_tickets"] == 0):
		commission["avg_commission"] = 0
		commission["commission"] = 0
	
	return jsonify(commission), 200

@misc_bp.route('/top-customer', methods=['GET'])
def top_customers_handler():
	# get booking agent username from session
	username = session['user']['username']
	# current_date = date.today().strftime("%Y-%m-%d")
	# default_date_6_months = (date.today() - timedelta(months=6)).strftime("%Y-%m-%d")
	# default_date_one_year = (date.today() - timedelta(years=1)).strftime("%Y-%m-%d")

	if username is None:
		return jsonify({"error": "you must login first"}), 400
	
	# get parameters from url
	start_date = request.args.get("start_date", None)
	end_date = request.args.get("end_date", None)
	limit = request.args.get("limit", None)

	# search for flight within a specific time period, default to 6 months
	# get the top customers in terms of number of tickets bought

	top_tickets_customer_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT customer_email, COUNT(*) AS num_tickets
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	GROUP BY customer_email
	ORDER BY num_tickets DESC
	LIMIT {limit}
	"""

	top_tickets_customer_query = top_tickets_customer_query_template.format(
		username=KV_ARG("booking_agent_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date)),
		limit=limit
	)

	db = current_app.config["db"]
	top_tickets_customer = db.execute_query(top_tickets_customer_query)
	top_tickets_result = []
	for row in top_tickets_customer:
		top_tickets_result.append({
			"customer_email": row[0],
			"num_tickets": row[1]
		})

	# search for flight within a specific time period, default to 1 year
	# get the top customers in terms of total commission received

	top_commission_customer_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT customer_email, SUM(price * {COMMISSION_RATE}) AS commission
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	GROUP BY customer_email
	ORDER BY commission DESC
	LIMIT {limit}
	"""

	top_commission_customer_query = top_commission_customer_query_template.format(
		COMMISSION_RATE=COMMISSION_RATE,
		username=KV_ARG("booking_agent_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date)),
		limit=limit
	)

	top_commission_customer = db.execute_query(top_commission_customer_query)
	if top_commission_customer is None:
		return jsonify({"error": "Internal error"}), 500
	top_commission_result = []
	for row in top_commission_customer:
		top_commission_result.append({
			"customer_email": row[0],
			"commission": row[1]
		})
	
	return jsonify({
		"top_tickets_customer": top_tickets_result,
		"top_commission_customer": top_commission_result
	}), 200