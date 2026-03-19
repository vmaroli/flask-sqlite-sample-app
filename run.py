# run.py
# Application entry point
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run with debug mode for development
    # In production, use gunicorn or another WSGI server
    app.run(debug=True, port=5000)