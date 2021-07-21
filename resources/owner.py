from flask_restful import Resource
from models.owner import OwnerModel
from flask import request
from schemas.owner import OwnerSchema

owner_schema = OwnerSchema()


class OwnerRegister(Resource):
    @classmethod
    def post(cls):
        data = owner_schema.load(request.get_json())

        if OwnerModel.find_by_username(data["username"]):
            return {"message": "owner already exists"}

        owner = OwnerModel(**data)
        owner.save_to_database()

        return {"message": "owner created successfully!"}, 201


class OwnerList(Resource):
    def get(self):
        return {"Owners": [owner_schema.dump(owner) for owner in OwnerModel.query.all()]}
