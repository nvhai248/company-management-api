import os
from dotenv import load_dotenv

load_dotenv()


def get_connection_string():
    engine = os.environ.get("DB_ENGINE")
    host = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    return f"{engine}://{username}:{password}@{host}/{db_name}"


SQLALCHEMY_DB_URL = get_connection_string()
ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")

# JWT Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
