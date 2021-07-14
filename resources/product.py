from flask_restful import Resource, reqparse, inputs
from models.product import ProductModel
from models.store import StoreModel

class Product(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        self.parser.add_argument('name',
                type=str,
                required=False,
                help="fill that part"
        )

        self.parser.add_argument('genre',
                type=str,
                required=False,
                help="fill that part"
        )

        self.parser.add_argument('price',
                type=float,
                required=False,
                help="fill that part"
        )

        data = self.parser.parse_args()
        products = []
        for key, value in data.items():
            if key == 'name':
                product = ProductModel.find_by_name(value)
                return product.json()
            elif key == 'genre':
                products = ProductModel.find_by_genre(value)
            elif key == 'price':
                products = ProductModel.find_by_price(value)

        if len(products) != 0:
            return {"products": [prodcut.json() for prodcut in products]}
        else:
            return {"message": "product not found"}


    def post(self):
        self.parser.add_argument('name',
                type=str,
                required=True,
                help="fill that part"
        )

        self.parser.add_argument('description',
                type=str,
                required=False,
        )

        self.parser.add_argument('genre',
                type=str,
                required=True,
                help="fill that part"
        )

        self.parser.add_argument('available',
                type=inputs.boolean,
                required=True,
                help="fill that part"
        )

        self.parser.add_argument('price',
                type=float,
                required=True,
                help="fill that part"
        )
        self.parser.add_argument('store_id',
                type=int,
                required=True,
                help="fill that part"
        )

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
        self.parser.add_argument('name',
                type=str,
                required=True,
        )

        data = self.parser.parse_args()
        name = data['name']
        product = ProductModel.find_by_name(name)
        if product:
            try:
                product.delete_from_database()
                return {"message": "{} deleted".format(name)}
            except:
                return {"message": "error while adding to database"}, 500
        else:
            return {"message": "no product named {}".format(name)}

    def put(self):
        self.parser.add_argument('name',
                type=str,
                required=True,
                help="fill that part"
        )

        self.parser.add_argument('description',
                type=str,
                required=False,
        )

        self.parser.add_argument('genre',
                type=str,
                required=False,
                help="fill that part"
        )

        self.parser.add_argument('available',
                type=inputs.boolean,
                required=False,
                help="fill that part"
        )

        self.parser.add_argument('price',
                type=float,
                required=False,
                help="fill that part"
        )

        data = self.parser.parse_args()
        if not data['name']:
            return {"message": "type name of product you want to update"}
        product = ProductModel.find_by_name(data['name'])
        print(product.json())
        if not product:
            return {"message": "no product named {}".format(data['name'])}
        for key, value in data.items():
            if not value:
                continue
            if key == 'genre':
                product.genre = value
            if key == 'price':
                product.price = value
            if key == 'description':
                product.description = value
            if key == 'available':
                product.available = value
        print(product.json())
        try:
            product.save_to_database()
        except:
            return {"message": "error updating database"}, 500
        return {"message": "product updated"}


class ProductList(Resource):
    def get(self):
        return {"products": [product.json() for product in ProductModel.query.all()]}
