import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV")
    DATABASE_TYPE = os.getenv("DATABASE_TYPE")
    
    if DATABASE_TYPE == "sqlite":
        SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    else:
        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_DBNAME = os.getenv("MONGODBNAME")
