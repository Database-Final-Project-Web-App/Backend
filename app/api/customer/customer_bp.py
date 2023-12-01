from flask import Blueprint, current_app, session, jsonify, request

from .flight.flight_bp import flight_bp
from .ticket.ticket_bp import ticket_bp
from .misc.misc_bp import misc_bp

from app.utils.db import KV_ARG

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

# register blueprints
customer_bp.register_blueprint(flight_bp, url_prefix=flight_bp.url_prefix)
customer_bp.register_blueprint(ticket_bp, url_prefix=ticket_bp.url_prefix)
customer_bp.register_blueprint(misc_bp, url_prefix=misc_bp.url_prefix)

# get customer info
@customer_bp.route('/whoami', methods=["GET"])
def info_handler():
	db = current_app.config["db"]
	if 'user' not in session or session['user']['type'] != 'customer':
		# breakpoint()
		return jsonify({
			"status": 'error',
			"message": 'You must be logged in as a customer to access this information.'
		}), 401
	
	username = session['user']['username']
	query_template = \
	"""
	SELECT *
	FROM customer
	WHERE email = {username}
	"""
	query = query_template.format(
		username=KV_ARG("username", "string", username)
	)

	query_result = db.execute_query(query)
	if not query_result:
		return jsonify({
			"status": 'error',
			"message": 'User does not exist.'
		}), 401
	
	return jsonify({
		"status": 'success',
		"message": 'User info retrieved successfully.',
		"data": query_result[0]
	}), 200
	

	