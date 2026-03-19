import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the-top-secret-key'

    # SQLite database URI - stores the database file in the database folder
    # The three slashes indicate a relative path from the current directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database', 'app.db')

    # Disable modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False