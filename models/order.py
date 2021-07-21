from database import database

# date is String, try to make it date object


class OrderModel(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey("users.id"), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    total_price = database.Column(database.Float(precision=3))
    order_date = database.Column(database.String(80), nullable=False)

    user = database.relationship("UserModel", viewonly=True)
    product = database.relationship("ProductModel", viewonly=True)

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()
