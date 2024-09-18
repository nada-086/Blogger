from flask_sqlalchemy import SQLAlchemy
from injector import inject
from app.models.sql.user import User
from app.models.sql.blog import Blog
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

class SQLiteUserService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, email, password):
        user = self.db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return True
        return False

    def signup(self, name, email, password):
        if self.db.session.query(User).filter_by(email=email).first():
            return None
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role='Reader')
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def get_user_by_email(self, email):
        return self.db.session.query(User).filter_by(email=email).first()

    def get_readers_and_authors(self):
        return self.db.session.query(User).filter(User.role.in_(['Reader', 'Author'])).all()

    def promote_user(self, user_id):
        user = self.db.session.query(User).filter_by(id=user_id).first()
        if user:
            if user.role == 'Reader':
                user.role = 'Author'
            elif user.role == 'Author':
                user.role = 'Admin'
            self.db.session.commit()
        return user

    def get_user_blogs(self, user_id):
        return self.db.session.query(Blog).filter_by(author_id=user_id).all()

    def get_non_admin_blogs(self):
        non_admin_users = self.db.session.query(User).filter(User.role != 'Admin').all()
        non_admin_user_ids = [user.id for user in non_admin_users]
        return self.db.session.query(Blog).filter(Blog.author_id.in_(non_admin_user_ids)).all()