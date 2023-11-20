from flask import Blueprint

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')

@misc_bp.route('/commision', methods=['GET'])
def commision_handler():
	#TODO:
	return 'commision'

@misc_bp.route('/top-customer', methods=['GET'])
def top_customers_handler():
	#TODO:
	return 'top customer'