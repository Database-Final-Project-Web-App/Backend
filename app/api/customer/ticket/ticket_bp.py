from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime

from app.utils.db import KV_ARG, V_ARG, ticket_left

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket_bp.route('/purchase', methods=["POST"])
def purchase_handler():
	"""
	input: flight_num

	
	"""
	# get username from session
	username = session["user"]["username"]
	if username is None:
		return jsonify({"error": "Please login first."}), 400
	
	# get flight_num from url parameter
	flight_num = request.args.get("flight_num", None)

	# get flight info
	search_query_template = \
	"""
	SELECT airline_name
	FROM flight
	WHERE flight_num = {flight_num}
	"""

	search_query = search_query_template.format(
		flight_num=KV_ARG("flight_num", "string", flight_num)
	)

	db = current_app.config["db"]
	airline_name = db.execute_query(search_query)["airline_name"]

	# check whether there is a ticket left
	ticket_left_result = ticket_left(db, flight_num, airline_name)
	if not ticket_left_result:
		return jsonify({"error": "No ticket left."}), 400
	
	# get purchase date
	purchase_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	

	# insert into ticket table
	insert_query_template = \
	"""
	INSERT INTO ticket (flight_num, airline_name, customer_email, booking_agent_id, purchase_date)
	VALUES (
		{flight_num},
		{airline_name},
		{customer_email},
		{booking_agent_id},
		{purchase_date},
	)
	"""
	insert_query = insert_query_template.format(
		flight_num=V_ARG("string", flight_num),
		airline_name=V_ARG("string", airline_name),
		customer_email=V_ARG("string", username),
		booking_agent_id=V_ARG("string", None),
		purchase_date=V_ARG("datetime", purchase_datetime)
	)

	try:
		db.execute_query(insert_query)
	except Exception:
		return jsonify({"error": "Already purchased the ticket."}), 400

	return jsonify({"status": "Successfully purchased the ticket."}), 200