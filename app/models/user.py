from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(50), default='Reader')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_author(self):
        return self.role == 'author'

    def __repr__(self):
        return f'<User {self.name}>'
