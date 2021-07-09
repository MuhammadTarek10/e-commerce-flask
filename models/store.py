from database import database


class StoreModel(database.Model):
    __tablename__ = 'stores'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    owner_id = database.Column(database.Integer, database.ForeignKey('owners.id'))

    products = database.relationship('ProductModel', lazy='dynamic')
    owner = database.relationship('OwnerModel', viewonly=True)


    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id

    def json(self):
        return {"name": self.name, "store_id": self.id, "owner": self.owner.username, "products": [product.json() for product in self.products.all()]}

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
