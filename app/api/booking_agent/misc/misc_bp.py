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
	total_query_template = \
	"""
	WITH my_ticket AS
	(SELECT *
	FROM ticket JOIN flight
	USING (flight_id, airline_name))
	SELECT SUM(price * {commision_rate}) AS commision, COUNT(*) AS num_tickets, AVG(price * {commision_rate}) AS avg_commision
	"""
	return 'commision'

@misc_bp.route('/top-customer', methods=['GET'])
def top_customers_handler():
	#TODO:
	return 'top customer'