from flask import Flask, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from mongoengine import connect
from bson import ObjectId

db = SQLAlchemy()

def create_app():
    # Create Flask Application
    app = Flask(__name__)

    # Load the Configuration
    app.config.from_object(Config)

    # Initialize the correct database based on configuration
    if Config.DATABASE_TYPE == 'sqlite':
        db.init_app(app)
    else:
        connect(
            db=app.config['MONGO_DBNAME'],
            host=app.config['MONGO_URI']
        )

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
        if Config.DATABASE_TYPE == 'sqlite':
            from app.models.sql.user import User
            return User.query.get(user_id)
        else:
            from app.models.mongo.user import User
            try:
                return User.objects.get(id=user_id)
            except Exception:
                return None

    return app