# app/routes.py
# Flask routes demonstrating CRUD operations with SQLite
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.database import db
from app.models import User, Post

main_bp = Blueprint('main', __name__)


# ===== HTML Routes (UI) =====

@main_bp.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@main_bp.route('/users-page')
def users_page():
    """Display users page with all users"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('users.html', users=users)


@main_bp.route('/users/add', methods=['POST'])
def add_user():
    """Handle form submission to add a new user"""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate
    if not username or not email or not password:
        flash('All fields are required!', 'error')
        return redirect(url_for('main.users_page'))

    # Check if user exists
    if User.query.filter_by(username=username).first():
        flash(f'Username "{username}" already exists!', 'error')
        return redirect(url_for('main.users_page'))

    if User.query.filter_by(email=email).first():
        flash(f'Email "{email}" already exists!', 'error')
        return redirect(url_for('main.users_page'))

    try:
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )
        db.session.add(user)
        db.session.commit()
        flash(f'User "{username}" created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating user: {str(e)}', 'error')

    return redirect(url_for('main.users_page'))


@main_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_form(user_id):
    """Handle form submission to delete a user"""
    user = User.query.get_or_404(user_id)
    username = user.username

    try:
        # Delete associated posts first
        Post.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{username}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')

    return redirect(url_for('main.users_page'))


@main_bp.route('/posts-page')
def posts_page():
    """Display posts page with all posts"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    users = User.query.order_by(User.username).all()
    return render_template('posts.html', posts=posts, users=users)


@main_bp.route('/posts/add', methods=['POST'])
def add_post():
    """Handle form submission to add a new post"""
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = request.form.get('user_id')
    published = request.form.get('published') == '1'

    # Validate
    if not title or not content or not user_id:
        flash('Title, content, and author are required!', 'error')
        return redirect(url_for('main.posts_page'))

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        flash('Invalid user selected!', 'error')
        return redirect(url_for('main.posts_page'))

    try:
        post = Post(
            title=title,
            content=content,
            user_id=user_id,
            published=published
        )
        db.session.add(post)
        db.session.commit()
        flash(f'Post "{title}" created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating post: {str(e)}', 'error')

    return redirect(url_for('main.posts_page'))


@main_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post_form(post_id):
    """Handle form submission to delete a post"""
    post = Post.query.get_or_404(post_id)
    title = post.title

    try:
        db.session.delete(post)
        db.session.commit()
        flash(f'Post "{title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting post: {str(e)}', 'error')

    return redirect(url_for('main.posts_page'))


# ===== API Routes (JSON) =====

@main_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    Expects JSON body with username, email, and password.
    """
    data = request.get_json()

    # Validate required fields
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    try:
        # Create new user instance
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password'])  # Hash the password
        )

        # Add to session and commit to database
        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_dict()), 201

    except Exception as e:
        # Roll back the session on any error
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def hash_password(password):
    """
    Hash a password for storage.
    In production, use werkzeug.security or bcrypt.
    """
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

@main_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users with optional pagination.
    Query params: page (default 1), per_page (default 10)
    """
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Limit per_page to prevent excessive data retrieval
    per_page = min(per_page, 100)

    # Query with pagination
    # paginate() returns a Pagination object with items and metadata
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False  # Return empty list instead of 404 for invalid pages
    )

    return jsonify({
        'users': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })


@main_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a single user by ID.
    Returns 404 if user not found.
    """
    # get_or_404 automatically returns 404 if not found
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@main_bp.route('/users/search', methods=['GET'])
def search_users():
    """
    Search users by username or email.
    Query param: q (search term)
    """
    query = request.args.get('q', '')

    if not query:
        return jsonify({'users': []})

    # Use LIKE for partial matching
    # The % wildcards match any characters before and after the search term
    search_term = f'%{query}%'

    users = User.query.filter(
        db.or_(
            User.username.ilike(search_term),  # Case-insensitive match
            User.email.ilike(search_term)
        )
    ).limit(20).all()

    return jsonify({'users': [user.to_dict() for user in users]})

@main_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user.
    Only updates fields that are provided in the request body.
    """
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Update only the fields that are provided
        if 'username' in data:
            # Check if new username is already taken by another user
            existing = User.query.filter_by(username=data['username']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Username already taken'}), 409
            user.username = data['username']

        if 'email' in data:
            # Check if new email is already taken by another user
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email already taken'}), 409
            user.email = data['email']

        if 'is_active' in data:
            user.is_active = data['is_active']

        # Commit changes to database
        # updated_at will be automatically set by onupdate
        db.session.commit()

        return jsonify(user.to_dict())

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@main_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID.
    Also deletes all associated posts (cascade).
    """
    user = User.query.get_or_404(user_id)

    try:
        # Delete associated posts first (if cascade not configured)
        Post.query.filter_by(user_id=user_id).delete()

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500