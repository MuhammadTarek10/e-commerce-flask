from database import database


class StoreModel(database.Model):
    __tablename__ = 'stores'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))

    products = database.relationship('ProductModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "Store id": self.id, "Products": [product.json() for product in self.products.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()
