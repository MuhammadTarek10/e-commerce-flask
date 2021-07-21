from flask_restful import Resource
from flask import request
from models.owner import OwnerModel
from marshmallow import ValidationError
from schemas.owner import OwnerSchema

owner_schema = OwnerSchema()


class OwnerRegister(Resource):

    def post(self):

        try:
            owner_data = owner_schema.load(request.get_json())
        except ValidationError as err:
            return err.message, 400

        owner = OwnerModel.find_by_username(owner_data['username'])
        email_exists = OwnerModel.if_email_exists(owner_data['email'])

        if owner:
            return {"message": "owner already exists"}
        if email_exists:
            return {"message": "email already exists"}

        owner = OwnerModel(**owner_data)
        owner.save_to_database()

        return {"message": "owner created successfully!"}, 201


class OwnerList(Resource):
    def get(self):
        return {"Owners": [owner_schema.dump(owner) for owner in OwnerModel.query.all()]}
