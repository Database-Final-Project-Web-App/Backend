from flask import Blueprint

booking_agent_bp = Blueprint('booking_agent', __name__, url_prefix='/booking-agent')

@booking_agent_bp.route('/all', methods=["GET"])
def all_handler():
	#TODO:
	return 'all booking agent'

@booking_agent_bp.route('/add', methods=["POST"])
def add_handler():
	#TODO:
	return 'add booking agent'