from mongoengine import DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from app.models.mongo.user import User
from app.models.mongo.blog import Blog
from injector import inject

class MongoUserService:
    @inject
    def __init__(self):
        pass

    def login(self, email, password):
        try:
            user = User.objects.get(email=email)
            if user and check_password_hash(user.password, password):
                login_user(user)
                return True
        except DoesNotExist:
            pass
        return False

    def signup(self, name, email, password):
        if User.objects(email=email).first():
            return None
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role='Reader')
        new_user.save()
        return new_user

    def get_user_by_email(self, email):
        return User.objects(email=email).first()

    def get_readers_and_authors(self):
        return User.objects(role__in=['Reader', 'Author'])

    def promote_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.role == 'Reader':
                user.role = 'Author'
            elif user.role == 'Author':
                user.role = 'Admin'
            user.save()
            return user
        except DoesNotExist:
            return None

    def get_user_blogs(self, user_id):
        return Blog.objects(author_id=user_id)

    def get_non_admin_blogs(self):
        non_admin_users = User.objects(role__ne='Admin')
        non_admin_user_ids = [user.id for user in non_admin_users]
        return Blog.objects(author_id__in=non_admin_user_ids)