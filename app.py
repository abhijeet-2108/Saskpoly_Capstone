# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    load_dotenv()  # Load env vars from .env file
    # print(os.getenv('DATABASE_URL'))  # This will show the value loaded from .env file

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Init DB and CSRF
    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from routes.main_routes import main_routes
    from routes.reporting_routes import reporting_routes 
    app.register_blueprint(main_routes)
    app.register_blueprint(reporting_routes)

    # 404 handler (must be inside create_app to be app-aware)
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
