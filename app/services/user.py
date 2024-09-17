from app.models.user import User
from app.models.blog import Blog
from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from app import db


class UserService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return False
        login_user(user)
        return True
    
    def signup(self, name, email, password):
        user_found = db.session.query(User).filter_by(email=email).first()
        if user_found:
            return None
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role='Reader')
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user
    
    def get_user_by_email(self, email):
        return db.session.query(User).filter_by(email=email).first()


    def list_users(self):
        return self.db.session.query(User).all()
    

    def get_readers_and_authors(self):
        return self.db.session.query(User).filter(User.role.in_(['Reader', 'Author'])).all()

    
    def promote_user(self, user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return None
        if user.role == 'Reader':
            user.role = "Author"
        elif user.role == "Author":
            user.role = "Admin"
        self.db.session.commit()
        return user

    def get_user_blogs(self):
        blogs = db.session.query(Blog).filter_by(author_id=current_user.id).all();
        return blogs
    
    def get_non_admin_blogs(self):
        non_admin_users = self.db.session.query(User).filter(User.role != 'Admin').all()
        non_admin_user_ids = [user.id for user in non_admin_users]
        blogs = self.db.session.query(Blog).filter(Blog.author_id.in_(non_admin_user_ids)).all()
        return blogs