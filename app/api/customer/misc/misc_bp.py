from flask import Blueprint

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')

@misc_bp.route('/spending', methods=["GET"])
def spending_handler():
	#TODO:
	return 'spending'