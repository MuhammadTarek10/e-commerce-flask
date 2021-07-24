import os

DEBUG=False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE", "sqlite:///database.db/")
