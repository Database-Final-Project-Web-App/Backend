from flask import Flask, jsonify, request
from flask_cors import CORS 
import pymysql.cursors
import traceback

from app.utils.db import DB
from app.utils.misc import *

config_path = "config/dummy_config.json"

app = Flask(__name__)
# allow CORS from frontend server
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

db = DB(config_path)

@app.route('/')
def index():
	return 'Hello, World!'

"""
Api for data
Example: http://localhost:5000/api/data/flight&status=InProgress
"""
@app.route('/api/data/flight')
def get_data():
	# table = request.args.get('table')
	table = "flight"
	status = request.args.get('status')
	try:
		query_template = "SELECT * FROM {table} WHERE status = '{status}';"
		query = query_template.format(
			table=table,
			status=status,
		)
		result = db.execute_query(query)
	except Exception as e:
		# return HTTP 400 Bad Request
		return jsonify({"error": str(e), "traceback": str(traceback.format_exc())}), 400

	return jsonify(result)

"""
API for login
Example: http://localhost:5000/api/login
"""
@app.route('/api/login', methods=['POST'])
def login():
	TODO("Add login API based on session")
	
	username = request.json['username']
	password = request.json['password']
	try:
		query_template = "SELECT * FROM user WHERE username = '{username}' AND password = '{password}';"
		query = query_template.format(
			username=username,
			password=password,
		)
		result = db.execute_query(query)
	except Exception as e:
		# return HTTP 400 Bad Request
		return jsonify({"error": str(e), "traceback": str(traceback.format_exc())}), 400

	return jsonify(result)


if __name__ == "__main__":
	app.run(port=5000)
