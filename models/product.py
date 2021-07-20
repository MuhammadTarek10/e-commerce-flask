from database import database
import numpy as np
from typing import Dict, List


class ProductModel(database.Model):
    __tablename__ = 'products'

    rate = 0

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), unique=True)
    description = database.Column(database.String(300))
    genre = database.Column(database.String(40))
    price = database.Column(database.Float(precision=2))
    available = database.Column(database.Boolean)

    store_id = database.Column(database.Integer, database.ForeignKey('stores.id'))
    store = database.relationship('StoreModel', viewonly=True)
    product_rate = database.relationship('RateToProductModel')
    order = database.relationship('OrderModel')

    def __init__(self, name: str, description: str, genre: str, price: float, available: bool, store_id: int):
        self.name = name
        self.description = description
        self.genre = genre
        self.price = price
        self.available = available
        self.store_id = store_id

    def json(self) -> Dict:
        return {
            "name": self.name, 
            "price": self.price, 
            "store_name": self.store.name, 
            "genre": self.genre, 
            "available" : self.available, 
            "rate": self.get_rate()
        }

    def get_rate(self):
        ave = []
        for rate_model in self.product_rate:
            ave.append(rate_model.rate)
        if len(ave) != 0:
            self.rate = np.mean(ave)
            return self.rate
        return 0

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    def save_to_database(self) -> None:
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self) -> None:
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def filter_rate(cls, rate: float) -> List:
        desired_products = []
        products = cls.query.all()
        for product in products:
            if rate <= product.get_rate():
                desired_products.append(product)
        return desired_products

    @classmethod
    def find_by_genre(cls, genre: str) -> List:
        return cls.query.filter_by(genre=genre).all()

    @classmethod
    def find_by_price(cls, price: float) -> List:
        return cls.query.filter(cls.price>=price).all()
