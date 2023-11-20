"""
- TODO: Separate api implementation into different files

- TODO: Make the server run on localhost:5000/api instead of localhost:5000

"""
from flask import Flask, jsonify, request, session
from flask_cors import CORS
# import pymysql.cursors
import traceback

from app.utils.db import DB
# from app.utils.misc import *

config_path = "config/dummy_config.json"

app = Flask(__name__)
# allow CORS from frontend server
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# set session secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# set session timeout to 1 hour
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# create db connection
db = DB(config_path)


@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'


@app.route('/api/data/flight', methods=["GET"])
def get_data():
    """
    Api for data
    Example: http://localhost:5000/api/data/flight&status=InProgress
    """
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
        return jsonify({
            "error": str(e),
            "traceback": str(traceback.format_exc())}
            ), 400

    return jsonify(result)


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    API for login
    Example: http://localhost:5000/api/login
    """
    # get username and password from the request form
    username = request.form.get('username')
    password = request.form.get('password')

    # check if username and password are valid using a query
    query_template = """
        SELECT * FROM customer
        WHERE email = '{username}'
        AND password = '{password}';
    """

    query = query_template.format(
        username=username,
        password=password,
    )
    result = db.execute_query(query)

    # if the query returns a result, then the username and password are valid
    if result:
        # set session variable
        session['username'] = username
        return jsonify({"message": "Login successful as {}".format(username)})
    else:
        return jsonify({"message": "Login failed!"}), 400


# get user info
@app.route('/api/data/user')
def get_user():
    """
    API for getting user info
    Example: http://localhost:5000/api/data/user
    """
    # the user will send HTTP GET request with a session cookie
    # the session cookie will contain the username

    # get username from session
    username = session.get('username')

    # if username is not set, then the user is not logged in
    if not username:
        return jsonify({"message": "User not logged in!"}), 400

    # check if username is valid using a query
    query_template = "SELECT * FROM customer WHERE email = '{username}';"
    query = query_template.format(
        username=username,
    )
    result = db.execute_query(query)

    # if the query returns a result, then the username is valid
    if result:
        return jsonify(result[0])
    else:
        return jsonify({"message": "User not logged in!"}), 400


# logout
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """
    API for logout
    Example: http://localhost:5000/api/logout
    """
    # invalidate the session
    session.clear()
    return jsonify({"message": "Logout successful!"})


if __name__ == "__main__":
    app.run(port=5000)
