from database import database


class StoreModel(database.Model):
    __tablename__ = "stores"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), unique=True, nullable=False)
    owner_id = database.Column(database.Integer, database.ForeignKey("owners.id"), nullable=False)

    products = database.relationship("ProductModel", lazy="dynamic")
    owner = database.relationship("OwnerModel")

    def json(self):
        return {
            "name": self.name,
            "store_id": self.id,
            "owner": self.owner.username,
            "products": [product.json() for product in self.products.all()],
        }

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
