from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime

from app.utils.db import KV_ARG, V_ARG, ticket_left
from app.utils.auth import is_logged_in, LOGINTYPE

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket_bp.route('/purchase', methods=["POST"])
def purchase_handler():
	"""
	input: flight_num

	
	"""
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session["user"]["username"]
	logintype = session["user"]["logintype"]
	if logintype != LOGINTYPE.CUSTOMER:
		return jsonify({"error": "You must login as customer."}), 400
	
	# get flight_num from url parameter
	data = request.get_json()
	flight_num = data.get("flight_num", None)
	airline_name = data.get("airline_name", None)
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

	db = current_app.config["db"]
	search_result=db.execute_query(search_query)
	if not search_result:
		return jsonify({"error": "Flight does not exist."}), 400

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
		customer_email=V_ARG("string", username),
		booking_agent_id=V_ARG("string", None),
		purchase_date=V_ARG("datetime", purchase_datetime)
	)

	result = db.execute_query(insert_query)
	if result is None:
		return jsonify({"error": "Internal error."}), 500
	db.commit()

	return jsonify({"status": "Successfully purchased the ticket."}), 200