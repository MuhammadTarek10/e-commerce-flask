from database import database
import numpy as np


class ProductModel(database.Model):
    __tablename__ = 'products'

    rate = 0

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    description = database.Column(database.String(300))
    genre = database.Column(database.String(40))
    price = database.Column(database.Float(precision=2))
    available = database.Column(database.Boolean)

    store_id = database.Column(database.Integer, database.ForeignKey('stores.id'))
    store = database.relationship('StoreModel', viewonly=True)
    product_rate = database.relationship('RateToProductModel')
    order = database.relationship('OrderModel')

    def __init__(self, name, description, genre, price, available, store_id):
        self.name = name
        self.description = description
        self.genre = genre
        self.price = price
        self.available = available
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price, "store_name": self.store.name, "genre": self.genre, "available" : self.available, "rate": self.get_rate()}

    def get_rate(self):
        ave = []
        for rate_model in self.product_rate:
            ave.append(rate_model.rate)
        self.rate = np.mean(ave)
        return self.rate

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def filter_rate(cls, rate):
        desired_products = []
        products = cls.query.all()
        for product in products:
            if rate <= product.get_rate():
                desired_products.append(product)
        return desired_products
