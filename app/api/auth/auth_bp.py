from flask import Blueprint, request, current_app, jsonify, session

from app.utils.db import KV_ARG, V_ARG, user_exists

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=["POST"])
def register_handler():

	# get parameters from request
	username = request.form.get('username')
	password = request.form.get('password')
	logintype = request.form.get('logintype')

	if logintype is None:
		return jsonify({
			"status": 'error',
			"message": "Logintype is required"
		}), 400

	if username is None or password is None:
		return jsonify({
			"status": 'error',
			"message": "Username and password are required"
		}), 400

	db = current_app.config["db"]

	exist = user_exists(db, username, logintype)
	if exist:
		return jsonify({
			"status": 'error',
			"message": "Username already exists"
		}), 400
			
	
	# register
	# define insert template and build query
	if logintype == 'customer':
		# get parameters from request
		name = request.form.get('name')
		building_number = request.form.get('building_number')
		street = request.form.get('street')
		city = request.form.get('city')
		state = request.form.get('state')
		phone_number = request.form.get('phone_number')
		passport_number = request.form.get('passport_number')
		passport_expiration = request.form.get('passport_expiration')
		passport_country = request.form.get('passport_country')
		date_of_birth = request.form.get('date_of_birth')

		insert_template = \
		"""
		INSERT INTO customer VALUES (
		{username}, 
		{name}, 
		{password}, 
		{building_number}, 
		{street}, 
		{city}, 
		{state}, 
		{phone_number}, 
		{passport_number}, 
		{passport_expiration}, 
		{passport_country}, 
		{date_of_birth})
		"""
		insert_query = insert_template.format(
			username=V_ARG("string", username),
			name=V_ARG("string", name),
			password=V_ARG("string", password),
			building_number=V_ARG("string", building_number),
			street=V_ARG("string", street),
			city=V_ARG("string", city),
			state=V_ARG("string", state),
			phone_number=V_ARG("string", phone_number),
			passport_number=V_ARG("string", passport_number),
			passport_expiration=V_ARG("datetime", passport_expiration),
			passport_country=V_ARG("string", passport_country),
			date_of_birth=V_ARG("datetime", date_of_birth)
		)

	elif logintype == 'booking agent':
		# get parameters from request
		booking_agent_id = request.form.get('booking_agent_id')
		airline_name = request.form.get('airline_name')

		insert_template = \
		"""
		INSERT INTO booking_agent VALUES (
		{username},  
		{password}, 
		{booking_agent_id},
		{airline_name})
		"""
		insert_query = insert_template.format(
			username=V_ARG("string", username),
			password=V_ARG("string", password),
			booking_agent_id=V_ARG("string", booking_agent_id),
			airline_name=V_ARG("string", airline_name)
		)

	elif logintype == 'staff':
		# get parameters from request
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		date_of_birth = request.form.get('date_of_birth')
		permission = request.form.get('permission')
		airline_name = request.form.get('airline_name')
		
		insert_template = \
		"""
		INSERT INTO airline_staff VALUES (
		{username},  
		{password}, 
		{first_name},
		{last_name},
		{date_of_birth},
		{permission},
		{airline_name})
		"""
		insert_query = insert_template.format(
			username=V_ARG("string", username),
			password=V_ARG("string", password),
			first_name=V_ARG("string", first_name),
			last_name=V_ARG("string", last_name),
			date_of_birth=V_ARG("datetime", date_of_birth),
			permission=V_ARG("string", permission),
			airline_name=V_ARG("string", airline_name)
		)

	db = current_app.config["db"]
	db.execute_query(insert_query)

	return jsonify({
		"status": 'success',
		"message": "Successfully registered"
	}), 200

@auth_bp.route('/login', methods=["POST"])
def login_handler():

	# get parameters from request
	username = request.form.get('username')
	password = request.form.get('password')
	logintype = request.form.get('logintype')

	# check whether user exists
	if logintype is None:
		return jsonify({
			"status": 'error',
			"message": "Logintype is required"
		}), 400

	if username is None or password is None:
		return jsonify({
			"status": 'error',
			"message": "Username and password are required"
		}), 400

	db = current_app.config["db"]

	exist = user_exists(db, username, logintype)
	if not exist:
		return jsonify({
			"status": 'error',
			"message": "Username does not exist or password is incorrect"
		}), 400
	
	# login
	# check whether the user already logged in

	session['user'] = {
		"username": username,
		"logintype": logintype
	}

	return jsonify({
		"status": 'success',
		"message": "Successfully logged in"
	}), 200

@auth_bp.route('/logout', methods=["POST"])
def logout_handler():
	session.pop('user', None)
	return jsonify({
		"status": 'success',
		"message": "Successfully logged out"
	}), 200
