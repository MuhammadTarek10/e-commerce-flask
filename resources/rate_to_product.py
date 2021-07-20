from flask_restful import Resource, reqparse
from models.rate_to_product import RateToProductModel
from models.user import UserModel
from models.product import ProductModel


class RateToPoduct(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_id", type=int, required=True, help="fill that part")

    parser.add_argument("product_id", type=int, required=True, help="fill that part")

    def get(self, rate):
        names = []
        products = ProductModel.filter_rate(rate)
        for product in products:
            name = ProductModel.find_by_id(product.id).name
            names.append(name)
        return {"products": names}

    def post(self, rate):
        data = self.parser.parse_args()

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "no user with that id"}

        if not ProductModel.find_by_id(data["product_id"]):
            return {"message": "no product with that id"}

        if RateToProductModel.already_rated(rate, **data):
            return {"message": "you already rated this product"}

        rate = RateToProductModel(rate, **data)
        try:
            rate.save_to_database()
        except:
            return {"message": "error while adding to database"}

        return {"message": "rated successfully"}
