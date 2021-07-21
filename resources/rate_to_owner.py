from flask_restful import Resource
from flask import request
from models.rate_to_owner import RateToOwnerModel
from models.user import UserModel
from models.owner import OwnerModel
from schemas.rate_to_owner import RateToOwnerSchema

rate_to_owner_schema = RateToOwnerSchema()


class RateToOwner(Resource):
    @classmethod
    def get(cls, rate):
        names = []
        owners = OwnerModel.filter_rate(rate)
        for owner in owners:
            name = OwnerModel.find_by_id(owner.id).username
            names.append(name)
        return {"owners": names}


    @classmethod
    def post(cls, rate):
        data = rate_to_owner_schema.load(request.get_json())
        data['rate'] = rate

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "no user with that id"}

        if not OwnerModel.find_by_id(data["owner_id"]):
            return {"message": "no owner with that id"}

        if RateToOwnerModel.already_rated(rate, **data):
            return {"message": "you already rated this owner"}

        rate = RateToOwnerModel(**data)
        try:
            rate.save_to_database()
        except:
            return {"message": "error while adding to database"}

        return {"message": "rated successfully"}
