from flask import Blueprint

airport_bp = Blueprint('airport', __name__, url_prefix='/airport')

@airport_bp.route('/add', methods=["POST"])
def add_handler():
	#TODO:
	return 'add airport'