from flask_restful import Resource
from flask import request
from models.rate_to_product import RateToProductModel
from models.user import UserModel
from models.product import ProductModel
from schemas.rate_to_product import RateToProductSchema

rate_to_product_schema = RateToProductSchema()


class RateToPoduct(Resource):
    @classmethod
    def get(cls, rate):
        names = []
        products = ProductModel.filter_rate(rate)
        for product in products:
            name = ProductModel.find_by_id(product.id).name
            names.append(name)
        return {"products": names}

    @classmethod
    def post(cls, rate):
        data = rate_to_product_schema.load(request.get_json())
        data['rate'] = rate

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "no user with that id"}

        if not ProductModel.find_by_id(data["product_id"]):
            return {"message": "no product with that id"}

        if RateToProductModel.already_rated(rate, **data):
            return {"message": "you already rated this product"}

        rate = RateToProductModel(**data)
        try:
            rate.save_to_database()
        except:
            return {"message": "error while adding to database"}

        return {"message": "rated successfully"}
