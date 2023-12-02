from flask import Blueprint, current_app, session, jsonify, request

from .flight.flight_bp import flight_bp
from .ticket.ticket_bp import ticket_bp
from .misc.misc_bp import misc_bp

from app.utils.db import KV_ARG

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

# register blueprints
customer_bp.register_blueprint(flight_bp, url_prefix=flight_bp.url_prefix)
customer_bp.register_blueprint(ticket_bp, url_prefix=ticket_bp.url_prefix)
customer_bp.register_blueprint(misc_bp, url_prefix=misc_bp.url_prefix)

	

	