from database import database


class ProductModel(database.Model):
    __tablename__ = 'products'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    description = database.Column(database.String(300))
    genre = database.Column(database.String(40))
    price = database.Column(database.Float(precision=2))
    available = database.Column(database.Boolean)

    store_id = database.Column(database.Integer, database.ForeignKey('stores.id'))
    store = database.relationship('StoreModel', viewonly=True)

    def __init__(self, name, description, genre, price, available, store_id):
        self.name = name
        self.description = description
        self.genre = genre
        self.price = price
        self.available = available
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price, "genre": self.genre, "store_id": self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()
