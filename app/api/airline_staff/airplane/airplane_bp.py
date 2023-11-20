from flask import Blueprint

airplane_bp = Blueprint('airplane', __name__, url_prefix='/airplane')

@airplane_bp.route('/add', methods=["POST"])
def add_handler():
	#TODO:
	return 'add airplane'