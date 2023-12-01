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

	search_query = search_query_template.format(
		flight_id=KV_ARG("flight_num", "string", flight_id)
	)

	db = current_app.config["db"]
	airline_name = db.execute(search_query)["airline_name"]

	# get purchase date
	purchase_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	

	# insert into ticket table
	insert_query_template = \
	"""
	INSERT INTO ticket (flight_id, airline_name, customer_email, booking_agent_id, purchase_date)
	VALUES (
		{flight_num},
		{airline_name},
		{customer_email},
		{booking_agent_id},
		{purchase_date},
	)
	"""
	insert_query = insert_query_template.format(
		flight_num=KV_ARG("flight_num", "string", flight_id, mode="restricted"),
		airline_name=KV_ARG("airline_name", "string", airline_name, mode="restricted"),
		customer_email=KV_ARG("customer_email", "string", username, mode="restricted"),
		booking_agent_id=KV_ARG("booking_agent_email", "string", None, mode="restricted"),
		purchase_date=KV_ARG("purchase_date", "datetime", purchase_datetime, mode="restricted")
	)

	try:
		db.execute(insert_query)
	except Exception:
		return jsonify({"error": "Already purchased the ticket."}), 400

	return jsonify({"status": "Successfully purchased the ticket."}), 200