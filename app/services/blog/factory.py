from injector import inject
from config import Config
from app.services.blog.sql import SQLiteBlogService
from app.services.blog.mongo import MongoBlogService


class BlogServiceFactory:
    @inject
    def __init__(self, sql_service: SQLiteBlogService, mongo_service: MongoBlogService):
        self.sql_service = sql_service
        self.mongo_service = mongo_service

    def get_service(self):
        if Config.DATABASE_TYPE == 'sqlite':
            return self.sql_service
        else:
            return self.mongo_service