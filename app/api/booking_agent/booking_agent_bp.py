from flask import Blueprint

from .flight.flight_bp import flight_bp
from .ticket.ticket_bp import ticket_bp
from .misc.misc_bp import misc_bp

booking_agent_bp = Blueprint('booking_agent', __name__, url_prefix='/booking-agent')

# register all blueprints here
booking_agent_bp.register_blueprint(flight_bp, url_prefix=flight_bp.url_prefix)
booking_agent_bp.register_blueprint(ticket_bp, url_prefix=ticket_bp.url_prefix)
booking_agent_bp.register_blueprint(misc_bp, url_prefix=misc_bp.url_prefix)

