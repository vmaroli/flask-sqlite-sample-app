# app/models.py
# SQLAlchemy model definitions for SQLite database
from datetime import datetime
from app.database import db

class User(db.Model):
    """
    User model representing the users table.
    Stores user account information.
    """
    # Explicitly set the table name
    __tablename__ = 'users'

    # Primary key - auto-incrementing integer
    id = db.Column(db.Integer, primary_key=True)

    # Username - must be unique and cannot be null
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Email - indexed for faster lookups
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Password hash - never store plain text passwords
    password_hash = db.Column(db.String(256), nullable=False)

    # Timestamps for auditing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Boolean flag with default value
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.username}>'

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

# app/models.py (continued)
# Relationship example: Users can have many Posts

class Post(db.Model):
    """
    Post model representing blog posts.
    Each post belongs to a single user.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Foreign key linking to the users table
    # This creates the relationship at the database level
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published = db.Column(db.Boolean, default=False)

    # Define the relationship to User
    # backref creates a reverse relationship (user.posts)
    # lazy='dynamic' returns a query object instead of loading all posts immediately
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return f'<Post {self.title}>'


class Tag(db.Model):
    """
    Tag model for categorizing posts.
    Demonstrates a many-to-many relationship.
    """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# Association table for many-to-many relationship between Posts and Tags
# This is a simple table without a model class
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


# Update Post model to include tags relationship
# Add this to the Post class:
# tags = db.relationship('Tag', secondary=post_tags, backref='posts')