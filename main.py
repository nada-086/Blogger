from app import create_app, db
from flask_injector import FlaskInjector, singleton
from app.services.blog.sql import SQLiteBlogService
from app.services.user.sql import SQLiteUserService
from app.services.blog.mongo import MongoBlogService
from app.services.user.mongo import MongoUserService
from config import Config

def configure(binder):
    if Config.DATABASE_TYPE == 'sqlite':
        binder.bind(SQLiteBlogService, to=SQLiteBlogService(db), scope=singleton)
        binder.bind(SQLiteUserService, to=SQLiteUserService(db), scope=singleton)
    else:
        binder.bind(MongoBlogService, to=MongoBlogService(), scope=singleton)
        binder.bind(MongoUserService, to=MongoUserService(), scope=singleton)

app = create_app()

if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    FlaskInjector(app=app, modules=[configure])
    app.run()
