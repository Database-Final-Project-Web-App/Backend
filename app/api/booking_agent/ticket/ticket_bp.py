from flask import Blueprint

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket_bp.route('/purchase', methods=['POST'])
def purchase_handler():
	#TODO:
	return 'purchase ticket'