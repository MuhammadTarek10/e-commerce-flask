from flask_restful import Resource, reqparse
from models.rate_to_owner import RateToOwnerModel
from models.user import UserModel
from models.owner import OwnerModel


class RateToOwner(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('user_id',
            type=int,
            required=True,
            help='fill that part'
    )

    parser.add_argument('owner_id',
            type=int,
            required=True,
            help='fill that part'
    )

    parser.add_argument('rate',
            type=float,
            required=True,
            help='fill that part'
    )

    def get(self):
        names = []
        data = self.parser.parse_args()
        owners = OwnerModel.filter_rate(data['rate'])
        for owner in owners:
            name = OwnerModel.find_by_id(owner.id).username
            names.append(name)
        return {"owners": names}

    def post(self, owner):
        data = self.parser.parse_args()

        if not UserModel.find_by_id(data['user_id']):
            return {"message": "no user with that id"}

        if not OwnerModel.find_by_id(data['owner_id']):
            return {"message": "no owner with that id"}

        if RateToOwnerModel.already_rated(**data):
                return {"message": "you already rated this owner"}

        rate = RateToOwnerModel(**data)
        try:
            rate.save_to_database()
        except:
            return {"message": "error while adding to database"}

        return {"message": "rated successfully"}
