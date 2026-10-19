import os


class Config:
    # Use environment variable, fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///local_test.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
