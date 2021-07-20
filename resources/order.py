from flask_restful import Resource, reqparse, inputs
from models.order import OrderModel
from models.product import ProductModel
from models.user import UserModel


class Order(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("user_id", type=int, required=True, help="fill that part")

    parser.add_argument("product_id", type=int, required=True, help="fill that part")

    parser.add_argument("quantity", type=int, required=True, help="fill that part")

    parser.add_argument("order_date", type=str, required=True, help="fill that part")

    def post(self):
        data = self.parser.parse_args()

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "no user with that id"}

        product = ProductModel.find_by_id(data["product_id"])
        if not product:
            return {"message": "no product with that id"}

        total_price = data["quantity"] * product.price

        order = OrderModel(total_price, **data)
        try:
            order.save_to_database()
        except:
            return {"message": "error in adding to database"}

        return order.json(), 201
