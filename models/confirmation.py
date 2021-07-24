from database import database
from uuid import uuid4
from time import time


CONFIRMATION_EXPIRATION_DELTA = 1800 #30 minutes

class ConfirmationModel(database.Model):
    __tablename__ = 'confirmations'

    id = database.Column(database.String(50), primary_key=True)
    expire_at = database.Column(database.Integer)
    confirmed = database.Column(database.Boolean, default=False)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"))
    user = database.relationship("UserModel")

    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self):
        return time() > self.expire_at

    def force_to_expire(self):
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_database()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()
