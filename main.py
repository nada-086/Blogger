from app import create_app, db
from flask_injector import FlaskInjector, singleton
from app.services.blog import BlogService
from app.services.user import UserService

def configure(binder):
    binder.bind(BlogService, to=BlogService(db), scope=singleton)
    binder.bind(UserService, to=UserService(db), scope=singleton)

app = create_app()

if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    FlaskInjector(app=app, modules=[configure])
    app.run()
