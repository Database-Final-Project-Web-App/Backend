from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime, date, timedelta

from app.utils.db import KV_ARG

from app.utils.misc import COMMISION_RATE

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')

@misc_bp.route('/commision', methods=['GET'])
def commision_handler():
	# get booking agent username from session
	username = session['user']['username']
	# current_date = date.today().strftime("%Y-%m-%d")
	# default_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")

	if username is None:
		return jsonify({"error": "you must login first"}), 400

	# get parameters from url
	start_date = request.args.get("start_date", None)
	end_date = request.args.get("end_date", None)

	# search for flight within a specific time period, default to 30 days
	# get the total commision, number of tickets sold, and average commision per ticket
	commision_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price * COMMISION_RATE) AS commision, COUNT(*) AS num_tickets, AVG(price * COMMISION_RATE) AS avg_commision
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	"""

	commision_query = commision_query_template.format(
		username=KV_ARG("booking_agent_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)

	db = current_app.config["db"]
	commision = db.execute_query(commision_query)
	commision = commision[0] if commision else (0.0, 0, 0.0)
	return jsonify({
		"commision": commision[0],
		"num_tickets": commision[1],
		"avg_commision": commision[2]
	}), 200

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
	# get the top customers in terms of total commision received

	top_commision_customer_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT customer_email, SUM(price * COMMISION_RATE) AS commision
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	GROUP BY customer_email
	ORDER BY commision DESC
	LIMIT {limit}
	"""

	top_commision_customer_query = top_commision_customer_query_template.format(
		username=KV_ARG("booking_agent_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date)),
		limit=limit
	)

	top_commision_customer = db.execute_query(top_commision_customer_query)
	top_commision_result = []
	for row in top_commision_customer:
		top_commision_result.append({
			"customer_email": row[0],
			"commision": row[1]
		})
	
	return jsonify({
		"top_tickets_customer": top_tickets_result,
		"top_commision_customer": top_commision_result
	}), 200