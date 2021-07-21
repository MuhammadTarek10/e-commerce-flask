from database import database


class UserModel(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(80))
    last_name = database.Column(database.String(80))
    username = database.Column(database.String(80))
    password = database.Column(database.String(80))
    email = database.Column(database.String(120))
    activated = database.Column(database.Boolean, default=False)

    rate_to_product = database.relationship("RateToProductModel")
    rate_to_owner = database.relationship("RateToOwnerModel")
    orders = database.relationship("OrderModel")

    def __init__(self, first_name, last_name, username, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

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
