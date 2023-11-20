from flask import Flask 

import app.utils as utils 
from app.api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def hello_world():
	return 'Hello, World!'

# run the app
if __name__ == '__main__':
	app.run(debug=True)