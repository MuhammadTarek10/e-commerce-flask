from database import database


class UserModel(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(80), nullable=False)
    last_name = database.Column(database.String(80), nullable=False)
    username = database.Column(database.String(80), nullable=False)
    password = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(120), nullable=False)

    rate_to_product = database.relationship("RateToProductModel")
    rate_to_owner = database.relationship("RateToOwnerModel")
    orders = database.relationship("OrderModel")

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
