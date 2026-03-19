# app/queries.py
# Advanced query examples for SQLite with Flask-SQLAlchemy
from datetime import datetime, timedelta
from app.database import db
from app.models import User, Post

def get_active_users_with_posts():
    """
    Get all active users who have at least one post.
    Uses a subquery to check for post existence.
    """
    # Subquery to find user IDs with posts
    users_with_posts = db.session.query(Post.user_id).distinct().subquery()

    # Filter users who are active AND have posts
    return User.query.filter(
        User.is_active == True,
        User.id.in_(users_with_posts)
    ).all()


def get_recent_posts(days=7):
    """
    Get posts created within the last N days.
    Orders by creation date, most recent first.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    return Post.query.filter(
        Post.created_at >= cutoff_date,
        Post.published == True
    ).order_by(Post.created_at.desc()).all()


def get_user_post_counts():
    """
    Get the number of posts per user.
    Uses GROUP BY and aggregate functions.
    """
    from sqlalchemy import func

    # Query returns tuples of (user_id, username, post_count)
    return db.session.query(
        User.id,
        User.username,
        func.count(Post.id).label('post_count')
    ).outerjoin(Post).group_by(User.id).all()

def execute_raw_query():
    """
    Execute raw SQL for complex queries.
    Always use parameterized queries to prevent SQL injection.
    """
    # Use text() for raw SQL with named parameters
    from sqlalchemy import text

    sql = text("""
        SELECT u.username, COUNT(p.id) as post_count
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        WHERE u.is_active = :is_active
        GROUP BY u.id
        HAVING COUNT(p.id) > :min_posts
        ORDER BY post_count DESC
    """)

    # Execute with parameters to prevent SQL injection
    result = db.session.execute(sql, {
        'is_active': True,
        'min_posts': 5
    })

    # Fetch all results as a list of dictionaries
    return [dict(row) for row in result.mappings()]

def transfer_posts(from_user_id, to_user_id):
    """
    Transfer all posts from one user to another.
    Uses a transaction to ensure atomicity.
    """
    try:
        # Start a transaction (happens automatically with session)

        # Verify both users exist
        from_user = User.query.get(from_user_id)
        to_user = User.query.get(to_user_id)

        if not from_user or not to_user:
            raise ValueError("One or both users not found")

        # Update all posts to new owner
        Post.query.filter_by(user_id=from_user_id).update({
            'user_id': to_user_id
        })

        # Commit the transaction
        db.session.commit()
        return True

    except Exception as e:
        # Roll back all changes if anything fails
        db.session.rollback()
        raise e