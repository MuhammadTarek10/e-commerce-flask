import os

DEBUG=True
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db/"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
JWT_SECRET_KEY = "Tarek"