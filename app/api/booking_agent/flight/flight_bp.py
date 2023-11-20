from flask import Blueprint

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/my', methods=['GET'])
def my_handler():
	#TODO:
	return 'my flight'
