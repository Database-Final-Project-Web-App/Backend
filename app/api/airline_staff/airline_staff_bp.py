from flask import Blueprint
from .airplane.airplane_bp import airplane_bp
from .flight.flight_bp import flight_bp
from .airport.airport_bp import airport_bp
from .booking_agent.booking_agent_bp import booking_agent_bp
from .misc.misc_bp import misc_bp

airline_staff_bp = Blueprint('airline_staff', __name__, url_prefix='/airline-staff')

# register blueprints
airline_staff_bp.register_blueprint(airplane_bp, url_prefix=airplane_bp.url_prefix)
airline_staff_bp.register_blueprint(flight_bp, url_prefix=flight_bp.url_prefix)
airline_staff_bp.register_blueprint(airport_bp, url_prefix=airport_bp.url_prefix)
airline_staff_bp.register_blueprint(booking_agent_bp, url_prefix=booking_agent_bp.url_prefix)
airline_staff_bp.register_blueprint(misc_bp, url_prefix=misc_bp.url_prefix)
