from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime

from app.utils.db import KV_ARG, V_ARG, user_exists, ticket_left
from app.utils.auth import is_logged_in, LOGINTYPE

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket_bp.route('/purchase', methods=['POST'])
def purchase_handler():
	"""
	input: flight_num

	
	"""
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session["user"]["username"]
	logintype = session["user"]["logintype"]
	if logintype != LOGINTYPE.BOOKING_AGENT:
		return jsonify({"error": "You must login as booking agent."}), 400

	# get parameters
	data = request.get_json()
	flight_num = data.get("flight_num", None)
	airline_name = data.get("airline_name", None)
	customer_email = data.get("customer_email", None)
	db = current_app.config["db"]

	if customer_email is None:
		return jsonify({"error": "You must have a customer."}), 400
	
	# check whether the customer exists
	#breakpoint()
	if not user_exists(db, customer_email, "customer")[0]:
		return jsonify({"error": "Customer does not exist."}), 400
	

	if flight_num is None or airline_name is None:
		return jsonify({"error": "Flight number and airline name are required."}), 400
	flight_num = int(flight_num)

	# check whether flight exists
	search_query_template = \
	"""
	SELECT *
	FROM flight
	WHERE {flight_num}
	AND {airline_name}
	"""

	search_query = search_query_template.format(
		flight_num=KV_ARG("flight_num", "number", flight_num, mode="restricted"),
		airline_name=KV_ARG("airline_name", "string", airline_name, mode="restricted")
	)

	search_result=db.execute_query(search_query)
	if not search_result:
		return jsonify({"error": "Flight does not exist."}), 400

	# check whether the booking agent works for the airline
	airline_query_template = \
	"""
	SELECT airline_name
	FROM booking_agent_workfor
	WHERE {username}
	"""

	airline_query = airline_query_template.format(
		username=KV_ARG("booking_agent_email", "string", username),
	)
	try:
		airline_result = db.execute_query(airline_query)
	except Exception:
		return jsonify({"error": "Internal error."}), 500
	airline_result = [airline[0] for airline in airline_result]
	# show the airline name that the booking agent works for
	if airline_name not in airline_result:
		return jsonify({"error": "Booking agent does not work for the airline. It only works for{}".format(airline_result)}), 400
	
	# check whether there is a ticket left
	ticket_left_result = ticket_left(db, flight_num, airline_name)
	if not ticket_left_result:
		return jsonify({"error": "No ticket left."}), 400
	
	
	# get purchase date
	purchase_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	

	# insert into ticket table
	insert_query_template = \
	"""
	INSERT INTO ticket (flight_num, airline_name, customer_email, booking_agent_email, purchase_date)
	VALUES (
		{flight_num},
		{airline_name},
		{customer_email},
		{booking_agent_id},
		{purchase_date}
	)
	"""
	insert_query = insert_query_template.format(
		flight_num=V_ARG("number", flight_num),
		airline_name=V_ARG("string", airline_name),
		customer_email=V_ARG("string", customer_email),
		booking_agent_id=V_ARG("string", username),
		purchase_date=V_ARG("datetime", purchase_datetime)
	)

	result = db.execute_query(insert_query)
	if result is None:
		return jsonify({"error": "Internal error."}), 500
	db.commit()

	return jsonify({"status": "Successfully purchased the ticket."}), 200