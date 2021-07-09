from database import database

class RateToProductModel(database.Model):
    __tablename__ = 'RateToProduct'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'))
    rate = database.Column(database.Float(precision=1))

    user = database.relationship('UserModel', viewonly=True)
    product = database.relationship('ProductModel', viewonly=True)

    def json(self):
        return {"user_id": self.user_id, "product_id": self.product_id, "rate": self.rate}

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    @classmethod
    def find_user_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

    @classmethod
    def find_product_by_id(cls, id):
        return cls.query.filter_by(product_id=id).first()
