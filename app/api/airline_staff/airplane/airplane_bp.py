from flask import Blueprint, jsonify, request, current_app, session
from app.utils.db import KV_ARG, find_airline, find_permission
from app.utils.auth import is_logged_in, LOGINTYPE, PERMISSION

airplane_bp = Blueprint('airplane', __name__, url_prefix='/airplane')

@airplane_bp.route('/add', methods=["POST"])
def add_handler():
	#TODO:
	# get username from session
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.AIRLINE_STAFF:
		return jsonify({"error": "You must login as airline staff."}), 400
	db = current_app.config["db"]
	permission = find_permission(db, username)
	if PERMISSION.ADMIN not in permission:
		return jsonify({"error": "You don't have the permission to add airplane."}), 400
	
	return 'add airplane'