from flask import Blueprint

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')


@misc_bp.route('/frequent-customer', methods=["GET"])
def frequent_customer_handler():
	#TODO:
	return 'frequent customer'


@misc_bp.route('/report', methods=["GET"])
def report_handler():
	#TODO:
	return 'report'


@misc_bp.route('/revenue-comparison', methods=["GET"])
def revenue_comparison_handler():
	#TODO:
	return 'revenue comparison'


@misc_bp.route('/top-destination', methods=["GET"])
def top_destination_handler():
	#TODO:
	return 'top destination'


@misc_bp.route('/grant-permission', methods=["POST"])
def grant_permission_handler():
	#TODO:
	return 'grant permission'