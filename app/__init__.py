from flask import Flask, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models.user import User


db = SQLAlchemy()

def create_app():
    # Create Flask Application
    app = Flask(__name__)

    # Load the Configuration
    app.config.from_object(Config)

    # Initialize the database and login manager
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Import and register blueprints inside the function to avoid circular imports
    from app.routes.blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix="/blogs")
    from app.routes.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")

    # Rendering the Home Page
    @app.route('/')
    def home():
        return redirect('/user/login')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
