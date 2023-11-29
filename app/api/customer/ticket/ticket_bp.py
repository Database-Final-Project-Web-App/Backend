from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime

from app.utils.db import KV_ARG

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket_bp.route('/purchase', methods=["POST"])
def purchase_handler():
	"""
	input: flight_id

	
	"""
	# get username from session
	username = session["user"]["username"]
	# get flight_id from url parameter
	flight_id = request.args.get("flight_id", None)

	# get flight info
	search_query_template = \
	"""
	SELECT airline_name
	FROM flight
	WHERE flight_id = {flight_id}
	"""


	# insert into ticket table
	insert_query_template = \
	"""
	INSERT INTO ticket
	VALUES (
		{ticket_id},
		{flight_id},
		{airline_name},
		{customer_email},
		{booking_agent_id},
		{purchase_date},
	)
	"""
	insert_query = insert_query_template.format(
		flight_id=KV_ARG("flight_id", "number", flight_id, mode="restricted"),
		airline_name=KV_ARG("airline_name", "string", airline_name, mode="restricted"),
		customer_email=KV_ARG("customer_email", "string", username, mode="restricted"),
		booking_agent_id=KV_ARG("booking_agent_email", "number", None, mode="restricted"),
		purchase_date=KV_ARG("purchase_date", "datetime", purchase_datetime, mode="restricted")
	)

	db = current_app.config["db"]
	try:
		db.execute(insert_query)
	except Exception:
		return jsonify({"error": "Already purchased the ticket."}), 400

	# return ticket
	ticket = []
	ticket.append({
		"customer_email": username,
		"flight_id": flight_id,
		"airline_name": airline_name,
		"arrival_time": arrival_time,
		"departure_time": departure_time,
		"price": price,
		"status": status,
		"airplane_id": airplane_id,
		"arr_airport_name": arr_airport_name,
		"dept_airport_name": dept_airport_name,
		"arr_city": arr_city,
		"dept_city": dept_city,
		"ticket_id": ticket_id,
		"purchase_datetime": purchase_datetime,
	})
	return jsonify({"ticket": ticket}), 200