from flask import Blueprint

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/search', methods=["GET"])
def search_handler():
	#TODO:
	return 'search flight'