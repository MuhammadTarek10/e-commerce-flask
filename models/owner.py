from database import database


class OwnerModel(database.Model):
    __tablename__ = 'owners'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80))
    password = database.Column(database.String(80))
    email = database.Column(database.String(120))

    store_id = database.Column(database.Integer, database.ForeignKey('stores.id'))
    store = database.relationship('StoreModel')

    def __init__(self, username, password, email, store_id):
        self.username = username
        self.password = password
        self.email = email
        self.store_id = store_id


    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def json(self):
        return {"username": self.username, "email": self.email}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
