from flask import Flask 

from app.utils.db import DB
from app.api import api_bp

db_config_path = "config/dummy_config.json"
db = DB(db_config_path)

app = Flask(__name__)

# add db to app config
app.config['db'] = db

# register api blueprint
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def hello_world():
	return 'Hello, World!'

# run the app
if __name__ == '__main__':
	app.run(debug=True)