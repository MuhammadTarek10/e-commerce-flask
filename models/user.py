from database import database
from flask import request, url_for
from requests import post
from models.confirmation import ConfirmationModel
from libs.mailgun import Mailgun


class UserModel(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(80))
    last_name = database.Column(database.String(80))
    username = database.Column(database.String(80), unique=True)
    password = database.Column(database.String(80))
    email = database.Column(database.String(120), unique=True)

    confirmation = database.relationship("ConfirmationModel", lazy='dynamic', cascade="all, delete-orphan")
    rate_to_product = database.relationship("RateToProductModel")
    rate_to_owner = database.relationship("RateToOwnerModel")
    orders = database.relationship("OrderModel")

    @property
    def most_recent_confirmation(self):
        return self.confirmation.order_by(database.desc(ConfirmationModel.expire_at)).first()

    def __init__(self, first_name, last_name, username, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation)
        subject = "Registration Confirmation"
        text = f"Hi, Click the link to confirm Registration: {link}"
        html = f'<html>Hi, Click the link to confirm Registration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_email([self.email], subject, text, html)

    def json(self):
        return {"username": self.username, "email": self.email}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
