from models import db, User
from werkzeug.security import generate_password_hash
from app import app

with app.app_context():
    # Create a new admin user if not exists
    username = 'admin'
    password = 'adminpassword'  # Replace with a secure password
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        admin_user = User(
            username=username,
            password=generate_password_hash(password),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")
    else:
        print(f"User '{username}' already exists.")
