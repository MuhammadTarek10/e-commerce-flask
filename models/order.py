from database import database
# date is String, try to make it date object

class OrderModel(database.Model):
    __tablename__ = 'orders'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'))
    quantity = database.Column(database.Integer)
    total_price = database.Column(database.Float(precision=3))
    order_date = database.Column(database.String(80))

    user = database.relationship('UserModel', viewonly=True)
    product = database.relationship('ProductModel', viewonly=True)

    def __init__(self, total_price, user_id, product_id, quantity, order_date):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date
        self.total_price = total_price

    def json(self):
        return {"user_id": self.user_id, "product_id": self.product_id, "quantity": self.quantity, "total_price": self.total_price, "order_date": self.order_date}


    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()
