from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(10), default='user') # role = admin/user

