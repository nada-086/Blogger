from injector import inject
from config import Config
from app.services.user.sql import SQLiteUserService
from app.services.user.mongo import MongoUserService


class UserServiceFactory:
    @inject
    def __init__(self, sql_service: SQLiteUserService, mongo_service: MongoUserService):
        self.sql_service = sql_service
        self.mongo_service = mongo_service

    def get_service(self):
        if Config.DATABASE_TYPE == 'sqlite':
            return self.sql_service
        else:
            return self.mongo_service