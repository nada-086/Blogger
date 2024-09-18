from flask import Blueprint, render_template, redirect, request
from flask_injector import inject
from flask_login import current_user, logout_user
from app.services.user.factory import UserServiceFactory

user = Blueprint("user", __name__)

@user.route('/')
def home():
    return redirect('/blogs')

@user.route('/login', methods=['GET'])
def login_form():
    return render_template("./user/login.html")

@user.route('/login', methods=['POST'])
@inject
def login(user_service: UserServiceFactory):
    service = user_service.get_service()
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return render_template("./user/login.html", message="All Fields are Required.")
    
    status = service.login(email=email, password=password)
    if not status:
        return render_template('./user/login.html', message="Please, Enter a Valid Username and Password.")
    return redirect('/blogs')

@user.route('/signup', methods=['GET'])
def signup_form():
    return render_template("./user/signup.html")

@user.route('/signup', methods=['POST'])
@inject
def signup(user_service: UserServiceFactory):
    service = user_service.get_service()
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not name or not email or not password:
        return render_template("./user/signup.html", message="All Fields are Required.")
    
    if service.get_user_by_email(email=email):
        return render_template('./user/signup.html', message="Email is Already Registered. Try to Log In.")
    
    user_created = service.signup(name=name, email=email, password=password)
    if not user_created:
        return render_template('/user/signup.html', message="Failed to create the user. Please try again.")
    
    return redirect('/user/login')

@user.route('/user-management', methods=['GET'])
@inject
def list_users(user_service: UserServiceFactory):
    service = user_service.get_service()
    if not current_user.is_admin():
        return render_template('./blog/list.html', message="Unauthorized Access")
    
    users = service.get_readers_and_authors()
    return render_template('./user/user-management.html', users=users)

@user.route('/promote_user/<user_id>')
@inject
def promote_user(user_service: UserServiceFactory, user_id):
    service = user_service.get_service()
    if not current_user.is_admin():
        return render_template('./blog/list.html', message="Unauthorized Access")
    
    user = service.promote_user(user_id)
    if not user:
        return render_template('./blog/list.html', message="User not found or promotion failed.")
    
    return redirect('/user/user-management')

@user.route('/profile', methods=['GET'])
@inject
def profile(user_service: UserServiceFactory):
    service = user_service.get_service()
    blogs = service.get_user_blogs(current_user.id)
    return render_template('./user/profile.html', user=current_user, blogs=blogs)

@user.route('/blog-management')
@inject
def blog_management(user_service: UserServiceFactory):
    service = user_service.get_service()
    if not current_user.is_admin():
        return render_template('./blog/list.html', message="Unauthorized Access")
    
    blogs = service.get_non_admin_blogs()
    return render_template('./user/blog-management.html', blogs=blogs)

@user.route('/logout')
def logout():
    logout_user()
    return redirect('/user/login')