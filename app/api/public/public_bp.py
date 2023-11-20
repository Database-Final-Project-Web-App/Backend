from flask import Blueprint

from .flight.flight_bp import flight_bp

public_bp = Blueprint('public', __name__, url_prefix='/public')

# register blueprints
public_bp.register_blueprint(flight_bp, url_prefix=flight_bp.url_prefix)

