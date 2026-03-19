# app/__init__.py
# Flask application factory with SQLite initialization
from flask import Flask
from config import Config
from app.database import db, init_db
from flask_migrate import Migrate

def create_app(config_class=Config):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    # Create the Flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from the config class
    app.config.from_object(config_class)

    # Ensure the instance folder exists for the SQLite database
    import os
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # Folder already exists

    # Initialize the database with this app
    init_db(app)
    migrate = Migrate(app, db) 

    # Register blueprints for routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app