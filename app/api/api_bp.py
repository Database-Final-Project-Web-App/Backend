from flask import Blueprint
from app.api.public import public_bp
from app.api.auth import auth_bp
from app.api.customer import customer_bp
from app.api.airline_staff import airline_staff_bp
from app.api.booking_agent import booking_agent_bp


api_bp = Blueprint('api', __name__)

# Register all blueprints here
api_bp.register_blueprint(public_bp, url_prefix=public_bp.url_prefix)
api_bp.register_blueprint(auth_bp, url_prefix=auth_bp.url_prefix)
api_bp.register_blueprint(airline_staff_bp, url_prefix=airline_staff_bp.url_prefix)
api_bp.register_blueprint(customer_bp, url_prefix=customer_bp.url_prefix)
api_bp.register_blueprint(booking_agent_bp, url_prefix=booking_agent_bp.url_prefix)
