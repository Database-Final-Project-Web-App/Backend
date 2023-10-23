from flask import Flask, jsonify
from flask_cors import CORS 
import pymysql.cursors

app = Flask(__name__)
# allow CORS from frontend server
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def index():
	return 'Hello, World!'

@app.route('/api/data')
def get_data():
	conn = pymysql.connect(
		host="localhost",
		user="root",
		password="",
		db="atrs",
		cursorclass=pymysql.cursors.DictCursor
	)

	try:
		with conn.cursor() as cursor:
			# the result is a list (table) of dictionaries (rows)
			cursor.execute("SELECT * FROM flight WHERE status='Upcoming';")
			rows = cursor.fetchall()
	finally:
		conn.close()

	return jsonify(rows)



if __name__ == "__main__":
	app.run(port=5000)
