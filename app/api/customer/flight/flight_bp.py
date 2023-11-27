from flask import Blueprint, jsonify

flight_bp = Blueprint('flight', __name__, url_prefix='/flight')

@flight_bp.route('/my', methods=["GET"])
def my_handler():
	
	#TODO:
	return jsonify({
		'message': 'my flight', 
		'data': [1,2,3,4,5]
		})