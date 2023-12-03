from flask import Blueprint, jsonify, request, current_app, session
from datetime import datetime, date, timedelta

from app.utils.db import KV_ARG
from app.utils.auth import is_logged_in, LOGINTYPE

misc_bp = Blueprint('misc', __name__, url_prefix='/misc')

@misc_bp.route('/spending', methods=["GET"])
def spending_handler():
	# get parameters
	if not is_logged_in():
		return jsonify({"error": "You must login first."}), 400
	username = session['user']['username']
	logintype = session['user']['logintype']
	if logintype != LOGINTYPE.CUSTOMER:
		return jsonify({"error": "You must login as customer."}), 400
	# current_date = date.today().strftime("%Y-%m-%d")
	# default_date = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
	# data = request.get_json()

	# get parameters from url
	start_date = request.args.get("start_date", None)
	end_date = request.args.get("end_date", None)

	# search for flight within a specific time period, default to 1 year, and get the total spending
	total_query_template = \
	"""
	WITH my_ticket AS
	(SELECT * 
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price) AS spending
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	"""
	
	total_query = total_query_template.format(
		username=KV_ARG("customer_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)

	db = current_app.config["db"]
	total_spending = db.execute_query(total_query)
	total_spending = float(total_spending[0][0]) if total_spending[0][0] else 0.0

	# get the monthly spending within a specific time period, default to 1 year
	monthly_query_template = \
	"""
	WITH my_ticket AS
	(SELECT * 
	FROM ticket JOIN flight
	USING (flight_num, airline_name))
	SELECT SUM(price) AS spending, YEAR(purchase_date) AS year,MONTH(purchase_date) AS month
	FROM my_ticket
	WHERE {username}
	AND {purchase_date}
	GROUP BY year, month
	"""

	monthly_query = monthly_query_template.format(
		username=KV_ARG("customer_email", "string", username),
		purchase_date=KV_ARG("purchase_date", "datetime", (start_date, end_date))
	)

	monthly_spending = db.execute_query(monthly_query)
	# monthly spending is a table with three rows: spending, year, month.
	# it should be formated a dictionary of the form
	# {(year, month): spending}
	m = {}
	for row in monthly_spending:
		# format to YYYY-MM
		m["{}-{:02}".format(row[1], row[2])] = float(row[0])
	monthly_spending = m

	# # Draw the bar chart for monthly spending, default to last 6 months
	# # x-axis: month
	# # y-axis: monthly spending
	# x = monthly_spending["month"]
	# y = monthly_spending["spending"]
	# plt.bar(x,y,width=0.8, bottom=0, align='edge', color='blue', linewidth=2)
	# for k, v in enumerate(y):
	# 	plt.text(k+0.4, v, v, ha='center', va='bottom')
	# plt.title("Monthly Spending from {} to {}".format(start_date, end_date))
	# plt.xlabel("Month")
	# plt.ylabel("Spending")
	# plt.savefig("app/static/images/spending.png")

	# breakpoint()

	return jsonify({
		"start_date": start_date,
		"end_date": end_date,
		"total_spending": total_spending,
		"monthly_spending": monthly_spending,
	}), 200