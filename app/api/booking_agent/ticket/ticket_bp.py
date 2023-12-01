from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime

from app.utils.db import KV_ARG, V_ARG, user_exists, ticket_left

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket_bp.route('/purchase', methods=['POST'])
def purchase_handler():
	"""
	input: flight_num

	
	"""
	# get username from session
	username = session["user"]["username"]
	if username is None:
		return jsonify({"error": "you must login first"}), 400
	
	# get flight_num from url parameter
	flight_num = request.args.get("flight_num", None)
	customer_email = request.args.get("customer_email", None)

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

	# search whether the booking agent works for the airline
	airline_query_template = \
	"""
	SELECT airline_name
	FROM booking_agent_works_for
	WHERE {username}
	"""

	airline_query = airline_query_template.format(
		username=KV_ARG("booking_agent_email", "string", username),
	)

	airline_result = db.execute_query(airline_query)
	airline_result = [airline["airline_name"] for airline in airline_result]
	if airline_name not in airline_result:
		return jsonify({"error": "Booking agent does not work for the airline."}), 400
	
	# check whether there is a ticket left
	ticket_left_result = ticket_left(db, flight_num, airline_name)
	if not ticket_left_result:
		return jsonify({"error": "No ticket left."}), 400
	
	# check whether the customer exists
	if not user_exists(db, customer_email, "customer")[0]:
		return jsonify({"error": "Customer does not exist."}), 400
	
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
		flight_num=V_ARG("string", flight_num),
		airline_name=V_ARG("string", airline_name),
		customer_email=V_ARG("string", customer_email),
		booking_agent_id=V_ARG("string", username),
		purchase_date=V_ARG("datetime", purchase_datetime)
	)

	try:
		db.execute_query(insert_query)
	except Exception:
		return jsonify({"error": "Already purchased the ticket."}), 400

	return jsonify({"status": "Successfully purchased the ticket."}), 200