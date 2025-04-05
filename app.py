from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db
from routes.main_routes import main_routes

# Initialize extensions
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_routes)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
