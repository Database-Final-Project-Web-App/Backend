from flask import Flask, render_template, url_for, request, session, redirect, jsonify
import pymysql
import traceback
import demo_db

app = Flask(__name__)

host = "localhost"
user = "root"
password = ""
database = "atrs"

connection = pymysql.connect(
	host=host,
	user=user,
	password=password,
	database=database
)

app.secret_key = b'12345'
@app.route('/')
def index():
	return 'Hello World!'

@app.route('/register', methods=['POST'])
def register():
	"""
	Api for register
	:return:
	"""
	username = request.form.get('username')
	password = request.form.get('password')
	logintype = request.form.get('logintype')
	# Queries
	cursor = connection.cursor()
	if logintype == 'customer':
		query = 'SELECT * FROM customer WHERE email = %s and password = %s'
	elif logintype == 'booking agent':
		query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s'
	elif logintype == 'staff':
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	else:
		raise Exception("You must choose a logintype.")
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()
	if data:
		# The user already exists.
		error = 'This user already exists.'
		return error, 400
	# register
	if logintype == 'customer':
		ins = 'INSERT INTO customer VALUES ()'
	elif logintype == 'booking agent':
		airline = request.form.get('airline')
		ins_ = 'INSERT INTO booking_agent VALUES ({username}, {password}, {airline})'

	elif logintype == 'staff':
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	#return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
	"""
	Api for login
	"""
	try:
		username = request.form.get('username')
		password = request.form.get('password')
		logintype = request.form.get('logintype')
		# password = "password1"
		# logintype = "customer"
		# Queries
		cursor = connection.cursor()
		if logintype == 'customer':
			query = 'SELECT name FROM customer WHERE email = %s and password = %s'
		elif logintype == 'booking agent':
			query = 'SELECT name FROM booking_agent WHERE email = %s and password = %s'
		elif logintype == 'staff':
			query = 'SELECT name FROM airline_staff WHERE username = %s and password = %s'
		else:
			raise Exception("Logintype can't be empty!")
		cursor.execute(query, (username, password))
		data = cursor.fetchone()
		cursor.close()
		if data:
			# Create a session for this user
			session['username'] = username
			session['logintype'] = logintype
			return 'Login successfully!'
		else:
			# Return the error message
			error = 'Invalid login or username'
			return error, 400
	except Exception as e:
		# return HTTP 400 Bad Request
		return jsonify({"error": str(e), "traceback": str(traceback.format_exc())}), 500



if __name__ == '__main__':
	app.run('127.0.0.1', 5000)