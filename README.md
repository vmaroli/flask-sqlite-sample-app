# Flask SQLite Sample Application

A sample web application built with Python Flask, SQLite, and Jinja templates demonstrating basic CRUD operations with a lightweight database.

## Features

- Flask web framework
- SQLite database integration
- SQLAlchemy ORM
- Flask-Migrate for database migrations
- Jinja2 templating
- User and Post management

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flask-sqlite-sample-app.git
cd flask-sqlite-sample-app
```

### 2. Create a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

### Initialize the Database

Run the database initialization script to create the necessary tables:

```bash
python init_db.py
```

This will create the SQLite database file at `database/app.db` with all required tables.

### Database Migrations (Optional)

If you need to make schema changes, use Flask-Migrate:

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Description of changes"

# Apply the migration
flask db upgrade
```

## Running the Application

### Development Mode

```bash
python run.py
```

The application will start on `http://localhost:5000` with debug mode enabled.

## Project Structure

```
flask-sqlite-sample-app/
├── app/
│   ├── __init__.py          # Application factory
│   ├── database.py          # Database configuration
│   ├── models.py            # Database models
│   ├── queries.py           # Database queries
│   ├── routes.py            # Application routes
│   ├── static/
│   │   └── style.css        # CSS styles
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── users.html
│       └── posts.html
├── database/
│   └── app.db              # SQLite database file (created after init)
├── migrations/             # Database migration files
├── config.py               # Application configuration
├── init_db.py             # Database initialization script
├── run.py                 # Application entry point
└── requirements.txt       # Python dependencies
```

## Configuration

The application uses `config.py` for configuration. Key settings:

- `SECRET_KEY`: Secret key for session management (set via environment variable)
- `SQLALCHEMY_DATABASE_URI`: Database connection string (defaults to SQLite)

### Environment Variables

You can override default settings using environment variables:

```bash
export SECRET_KEY='your-secret-key-here'
export DATABASE_URL='sqlite:///path/to/database.db'
```

## Usage

Once the application is running, navigate to:

- **Home Page**: `http://localhost:5000/`
- **Users**: `http://localhost:5000/users`
- **Posts**: `http://localhost:5000/posts`

## Development

### Adding New Features

1. Create or modify models in `app/models.py`
2. Update routes in `app/routes.py`
3. Create/modify templates in `app/templates/`
4. Run migrations if database schema changed

### Running Tests

```bash
# Add your test commands here
python -m pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## Troubleshooting

### Database Issues

If you encounter database errors:
1. Delete the `database/app.db` file
2. Run `python init_db.py` again

### Port Already in Use

If port 5000 is already in use, modify the port in `run.py`:

```python
app.run(debug=True, port=5001)  # Change to any available port
```

## Support

For issues and questions, please open an issue on the GitHub repository.
