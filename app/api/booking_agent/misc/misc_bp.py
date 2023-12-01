from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime, date, timedelta

from app.utils.db import KV_ARG

from app.utils.misc import COMMISION_RATE

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')

@misc_bp.route('/commision', methods=['GET'])
def commision_handler():
	#TODO:
	# get booking agent username from session
	username = session['user']['username']
	current_date = date.today().strftime("%Y-%m-%d")
	default_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")

	# get parameters from url
	start_date = request.args.get("start_date", default_date)
	end_date = request.args.get("end_date", current_date)

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
	return 'commision'

@misc_bp.route('/top-customer', methods=['GET'])
def top_customers_handler():
	#TODO:
	return 'top customer'