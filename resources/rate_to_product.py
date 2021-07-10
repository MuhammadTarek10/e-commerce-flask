from flask_restful import Resource, reqparse
from models.rate_to_product import RateToProductModel
from models.user import UserModel
from models.product import ProductModel

class RateToPoduct(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('user_id',
            type=int,
            required=True,
            help='fill that part'
    )

    parser.add_argument('product_id',
            type=int,
            required=True,
            help='fill that part'
    )

    parser.add_argument('rate',
            type=float,
            required=True,
            help='fill that part'
    )

    def post(self):
        data = self.parser.parse_args()

        if not UserModel.find_by_id(data['user_id']):
            return {"message": "no user with that id"}

        if not ProductModel.find_by_id(data['product_id']):
            return {"message": "no product with that id"}

        if RateToProductModel.already_rated(**data):
                return {"message": "you already rated this product"}

        rate = RateToProductModel(**data)
        try:
            rate.save_to_database()
        except:
            return {"message": "error while adding to database"}

        return rate.json(), 201
