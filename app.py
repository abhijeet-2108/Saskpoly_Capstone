# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    load_dotenv()  # Load env vars from .env file

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Init DB and CSRF
    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from routes.main_routes import main_routes
    app.register_blueprint(main_routes)

    return app
