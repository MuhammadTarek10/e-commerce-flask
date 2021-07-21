from flask_restful import Resource
from flask import request
from models.store import StoreModel
from models.owner import OwnerModel
from schemas.store import StoreSchema

store_schema = StoreSchema()


class Store(Resource):
    @classmethod
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        else:
            return {"message": "store named {} not found".format(name)}

    @classmethod
    def post(cls, name):
        data = store_schema.load(request.get_json())

        store = StoreModel.find_by_name(name)
        if store:
            if store.owner_id == data["owner_id"]:
                return {"message": "store {} already exists".format(data["name"])}

        if not OwnerModel.find_by_id(data["owner_id"]):
            return {"message": "no owner with that id"}

        data['name'] = name

        store = StoreModel(**data)
        try:
            store.save_to_database()
        except:
            return {"message": "error in saving to database"}, 500
        return store_schema.dump(store)

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_database()
            except:
                return {"message": "error in deleting from database"}, 500
        else:
            return {"message": "no store named {}".format(name)}


class StoreList(Resource):
    def get(self):
        return {"Stores": [store_schema.dump(store) for store in StoreModel.query.all()]}
