from flask_restful import Resource, inputs
from flask import request
from models.order import OrderModel
from models.product import ProductModel
from models.user import UserModel
from schemas.order import OrderSchema

order_schema = OrderSchema()

class Order(Resource):
    @classmethod
    def post(cls):
        data = order_schema.load(request.get_json())

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "no user with that id"}

        product = ProductModel.find_by_id(data["product_id"])
        if not product:
            return {"message": "no product with that id"}

        total_price = data["quantity"] * product.price
        data['total_price'] = total_price

        order = OrderModel(**data)
        try:
            order.save_to_database()
        except:
            return {"message": "error in adding to database"}

        return order_schema.dump(order), 201
