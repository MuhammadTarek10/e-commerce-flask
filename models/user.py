from database import database

class UserModel(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80))
    password = database.Column(database.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
