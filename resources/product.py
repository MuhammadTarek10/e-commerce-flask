from flask_restful import Resource, reqparse, inputs
from models.product import ProductModel
from models.store import StoreModel

class Product(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
            type=str,
            required=True,
            help="fill that part"
    )

    parser.add_argument('description',
            type=str,
            required=False,
    )

    parser.add_argument('genre',
            type=str,
            required=True,
            help="fill that part"
    )

    parser.add_argument('available',
            type=inputs.boolean,
            required=True,
            help="fill that part"
    )

    parser.add_argument('price',
            type=float,
            required=True,
            help="fill that part"
    )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="fill that part"
    )


    def get(self):
        pass


    def post(self):
        data = self.parser.parse_args()
        product = ProductModel.find_by_name(data['name'])
        if product:
            if product.store_id == data['store_id']:
                return {"message": "product already exists"}
        if not StoreModel.find_by_id(data['store_id']):
            return {"message": "no store with that id"}
        product = ProductModel(**data)

        try:
            product.save_to_database()
        except:
            return {"message": "error while adding to database"}, 500

        return product.json(), 201

    def delete(self):
        data = self.parser.parse_args()
        product = ProductModel.find_by_name(data['name'])
        if product:
            try:
                product.delete_from_database()
                return {"message": "{} deleted".format(data['name'])}
            except:
                return {"message": "error while adding to database"}, 500
        else:
            return {"message": "no product named {}".format(data['name'])}

    def put(self):
        pass


class ProductList(Resource):
    def get(self):
        return {"products": [product.json() for product in ProductModel.query.all()]}
