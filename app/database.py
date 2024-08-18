import os
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


def get_connection_string():
    engine = os.environ.get("DB_ENGINE")
    host = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    return f"{engine}://{username}:{password}@{host}/{db_name}"


SQLALCHEMY_DB_URL = get_connection_string()

engine = create_engine(SQLALCHEMY_DB_URL)
metadata = MetaData()

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
