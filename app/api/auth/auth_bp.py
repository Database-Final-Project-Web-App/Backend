from flask import Blueprint


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=["POST"])
def register_handler():
	#TODO:
	return 'Register page'

@auth_bp.route('/login', methods=["POST"])
def login_handler():
	#TODO:
	return 'Login page'

@auth_bp.route('/logout', methods=["POST"])
def logout_handler():
	#TODO:
	return 'Logout page'
