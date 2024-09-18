from mongoengine import Document, StringField, DateTimeField
from flask_login import UserMixin
from datetime import datetime

class User(Document, UserMixin):
    name = StringField(max_length=200, required=True)
    email = StringField(max_length=120, required=True, unique=True)
    password = StringField(max_length=200, required=True)
    role = StringField(max_length=50, default='Reader')
    date_added = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users',
        'indexes': [
            'email',  # Index on email for efficient lookup
        ]
    }

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
        return self.role == 'Author'

    def __repr__(self):
        return f'<User {self.name}>'
