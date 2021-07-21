from flask_restful import Resource, inputs
from flask import request
from models.product import ProductModel
from models.store import StoreModel
from schemas.product import ProductSchema


product_schema = ProductSchema()

class Product(Resource):
    @classmethod
    def get(cls, name):
        product = ProductModel.find_by_name(name)
        if product:
            return product_schema.dump(product)
        return {"message": "product {} not found".format(name)}

    def post(self, name):
        data = product_schema.load(request.get_json())
        product = ProductModel.find_by_name(name)
        if product:
            if product.store_id == data["store_id"]:
                return {"message": "product already exists"}
        if not StoreModel.find_by_id(data["store_id"]):
            return {"message": "no store with that id"}

        data['name'] = name
        product = ProductModel(**data)

        try:
            product.save_to_database()
        except:
            return {"message": "error while adding to database"}, 500

        return product_schema.dump(product), 201

    @classmethod
    def delete(cls, name):
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
        pass


class ProductPrice(Resource):
    def get(self, price):
        print(ProductModel.find_by_price(price))
        return {
            "products": [
                product_schema.dump(product) for product in ProductModel.find_by_price(price)
            ]
        }


class ProductGenre(Resource):
    def get(self, genre):
        return {
            "products": [
                product_schema.dump(product) for product in ProductModel.find_by_genre(genre)
            ]
        }


class ProductList(Resource):
    def get(self):
        return {"products": [product_schema.dump(product) for product in ProductModel.query.all()]}
