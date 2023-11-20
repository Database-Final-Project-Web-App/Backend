from flask import Blueprint

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/my', methods=["GET"])
def my_handler():
	#TODO:
	return 'my flight'

@flight_bp.route('/create', methods=["POST"])
def create_handler():
	#TODO:
	return 'create flight'

@flight_bp.route('/change-status', methods=["POST"])
def change_status_handler():
	#TODO:
	return 'change flight status'

