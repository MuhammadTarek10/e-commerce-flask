from flask_restful import Resource, reqparse
from models.product import ProductModel



class Product(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('price',
            type=float,
            required=True,
            help="fill that part"
    )

    def get(self, name):
        product = ProductModel.find_by_name(name)
        if product:
            return product.json()

        return {"message": "product not found"}


    def post(self, name):
        if ProductModel.find_by_name(name):
            return {"message": "product already exists"}

        data = self.parser.parse_args()
        product = ProductModel(name, **data)

        product.save_to_database()

        # try:
        #     product.save_to_database()
        # except:
        #     return {"message": "error while adding to database"}, 500

        return product.json(), 201

class ProductList(Resource):
    def get(self):
        return {"products": [product.json() for product in ProductModel.query.all()]}
