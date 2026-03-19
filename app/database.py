# app/database.py
# Database setup and initialization utilities
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy database instance
# This will be initialized with the Flask app later
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask application.
    Creates all tables defined in the models.
    """
    db.init_app(app)

    # Create tables within the application context
    with app.app_context():
        # Import models here to ensure they are registered with SQLAlchemy
        from app import models

        # Create all tables that do not exist yet
        db.create_all()