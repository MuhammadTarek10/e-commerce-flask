from flask_restful import Resource, reqparse
from models.store import StoreModel
from models.owner import OwnerModel

class Store(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
            type=str,
            required=True,
            help="fill that part"
    )

    parser.add_argument('owner_id',
            type=int,
            required=True,
            help="fill that part"
    )

    def get(self):
        data = self.parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        if store:
            return store.json()
        else:
            return {"message": "store named {} not found".format(name)}

    def post(self):
        data = self.parser.parse_args()

        store = StoreModel.find_by_name(data['name'])
        if store:
            if store.owner_id == data['owner_id']:
                return {"message": "store {} already exists".format(data['name'])}

        if not OwnerModel.find_by_id(data['owner_id']):
            return {"message": "no owner with that id"}

        store = StoreModel(**data)
        try:
            store.save_to_database()
        except:
            return {"message": "error in saving to database"}, 500
        return store.json()

    def delete(self):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_database()
            except:
                return {"message": "error in deleting from database"}, 500
        else:
            return {"message": "no store named {}".format(data['name'])}

class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all()]}
