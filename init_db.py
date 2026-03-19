"""
Simple script to initialize the database.
Run this once to create the database tables.
"""
from app import create_app
from app.database import db

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
