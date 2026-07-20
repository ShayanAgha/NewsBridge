from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints (flat modules, no subpackages)
    from app.api_routes import api_bp
    from app.public_routes import public_bp
    from app.admin_routes import admin_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
