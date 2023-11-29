from flask import Flask
from flask_cors import CORS

from app.utils.db import DB
from app.api import api_bp

db_config_path = "config/dummy_config.json"
db = DB(db_config_path)

app = Flask(__name__)

# add db to app config
app.config['db'] = db

# register api blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# allow CORS from frontend server
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# set session secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# set session timeout to 1 hour
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

@app.route('/')
def hello_world():
	return 'Hello, World!'

# run the app
if __name__ == '__main__':
	app.run(debug=True)