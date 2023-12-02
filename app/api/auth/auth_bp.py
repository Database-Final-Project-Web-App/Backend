from flask import Blueprint, request, current_app, jsonify, session, make_response

from app.utils.db import KV_ARG, V_ARG, user_exists
from app.utils.misc import COOKIE_MAX_AGE
from app.utils.auth import is_logged_in, LOGINTYPE
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=["POST"])
def register_handler():

	# check whether user is logged in
	if is_logged_in():
		return jsonify({
			"status": 'error',
			"message": "User is already logged in"
		}), 400

	# get parameters from request
	data = request.get_json()
	username = data.get('username', None)
	password = data.get('password', None)
	logintype = data.get('logintype', None)

	if logintype is None:
		return jsonify({
			"status": 'error',
			"message": "Logintype is required"
		}), 400

	if not LOGINTYPE.is_valid(logintype):
		return jsonify({
			"status": 'error',
			"message": "You must choose a correct logintype. Instead, you chose {}".format(logintype)
		}), 400

	if username is None or password is None:
		return jsonify({
			"status": 'error',
			"message": "Username and password are required"
		}), 400

	db = current_app.config["db"]

	exist, result = user_exists(db, username, logintype)
	if exist:
		return jsonify({
			"status": 'error',
			"message": "Username already exists"
		}), 400
			
	
	# register
	# define insert template and build query
	if logintype == LOGINTYPE.CUSTOMER:
		# get parameters from request
		name = data.get('name', None)
		building_number = data.get('building_number', None)
		street = data.get('street', None)
		city = data.get('city', None)
		state = data.get('state', None)
		phone_number = data.get('phone_number', None)
		passport_number = data.get('passport_number', None)
		passport_expiration = data.get('passport_expiration', None)
		passport_country = data.get('passport_country', None)
		date_of_birth = data.get('date_of_birth', None)

		insert_template = \
		"""
		INSERT INTO customer (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth)
		VALUES (
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

	elif logintype == LOGINTYPE.BOOKING_AGENT:
		# get parameters from request
		airline_name = data.get('airline_name', None)

		# check if airline_name exists
		

		insert_template = \
		"""
		INSERT INTO booking_agent (email, password, airline_name) 
		VALUES (
		{username},  
		{password}, 
		{airline_name})
		"""
		insert_query = insert_template.format(
			username=V_ARG("string", username),
			password=V_ARG("string", password),
			airline_name=V_ARG("string", airline_name)
		)

	elif logintype == LOGINTYPE.AIRLINE_STAFF:
		# get parameters from request
		first_name = request.form.get('first_name', default=None)
		last_name = request.form.get('last_name', default=None)
		date_of_birth = request.form.get('date_of_birth', default=None)
		permission = request.form.get('permission', default=None)
		airline_name = request.form.get('airline_name', default=None)
		
		insert_template = \
		"""
		INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, airline_name) 
		VALUES (
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
	result = db.execute_query(insert_query)
	breakpoint()
	if (result is None):
		return jsonify({
			"status": 'error',
			"message": "Internal error"
		}), 500
	return jsonify({
		"status": 'success',
		"message": "Successfully registered"
	}), 200

@auth_bp.route('/login', methods=["POST"])
def login_handler():

	# check whether user is logged in
	if is_logged_in():
		return jsonify({
			"status": 'error',
			"message": "User is already logged in"
		}), 400

	# get parameters from request
	data = request.get_json()
	username = data.get('username', None)
	password = data.get('password', None)
	logintype = data.get('logintype', None)

	# validate parameters
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

	# define query template
	if logintype == LOGINTYPE.CUSTOMER:
		login_query_template = \
		"""
		SELECT * 
		FROM customer
		WHERE email = {username}
		AND password = {password}
		"""
	elif logintype == LOGINTYPE.BOOKING_AGENT:
		login_query_template = \
		"""
		SELECT * 
		FROM booking_agent
		WHERE email = {username}
		AND password = {password}
		"""
	elif logintype == LOGINTYPE.AIRLINE_STAFF:
		login_query_template = \
		"""
		SELECT * 
		FROM airline_staff
		WHERE username = {username}
		AND password = {password}
		"""
	else:
		# breakpoint()
		return jsonify({
			"status": 'error',
			"message": "You must choose a correct logintype. Instead, you chose {}".format(logintype)
		}), 400
	

	# build query
	login_query = login_query_template.format(
		username=V_ARG("string", username),
		password=V_ARG("string", password)
	)

	db = current_app.config["db"]
	query_result = db.execute_query(login_query, cursor_type="dict")

	# exist, query_result = user_exists(db, username, logintype, db_kwargs={"cursor_type": "dict"})
	# internal error
	if query_result is None:
		return jsonify({
			"status": 'error',
			"message": "Internal error"
		}), 500
	# login fail
	if len(query_result) == 0:
		return jsonify({
			"status": 'error',
			"message": "Failed to login as {}: Username does not exist or password is incorrect".format(logintype)
		}), 400

	username_display = ""
	if logintype == LOGINTYPE.CUSTOMER:
		username_display = query_result[0]['name']
	elif logintype == LOGINTYPE.BOOKING_AGENT:
		username_display = query_result[0]['email']
	elif logintype == LOGINTYPE.AIRLINE_STAFF:
		username_display = query_result[0]['first_name'] + " " + query_result[0]['last_name']
	else:
		raise Exception("You must choose a correct logintype.")

	session['user'] = {
		"username": username,
		"username_display": username_display,
		"logintype": logintype
	}

	response = make_response(jsonify({
		"status": 'success',
		"message": "Successfully logged in",
		"username_display": username_display,
	}), 200)
	
	response.set_cookie('username', username, max_age=COOKIE_MAX_AGE, path='/')
	response.set_cookie('username_display', username_display, max_age=COOKIE_MAX_AGE, path='/')
	response.set_cookie('logintype', logintype, max_age=COOKIE_MAX_AGE, path='/')

	return response


@auth_bp.route('/logout', methods=["POST"])
def logout_handler():
	session.pop('user', None)
	return jsonify({
		"status": 'success',
		"message": "Successfully logged out"
	}), 200

@auth_bp.route('/is_loggedin', methods=["GET"])
def current_user_handler():
	if 'user' in session:
		return jsonify({
			"status": 'success',
			"message": "User is logged in",
		}), 200
	else:
		return jsonify({
			"status": 'error',
			"message": "User is not logged in"
		}), 400