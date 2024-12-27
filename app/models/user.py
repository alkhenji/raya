from app.config.database import db
from flask_login import UserMixin
import hashlib
import os

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    salt = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # Generate a random salt
        self.salt = os.urandom(16).hex()
        # Hash password with salt
        self.password_hash = hashlib.sha256((password + self.salt).encode()).hexdigest()

    def check_password(self, password):
        # Check if hash matches
        return self.password_hash == hashlib.sha256((password + self.salt).encode()).hexdigest()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now()) 