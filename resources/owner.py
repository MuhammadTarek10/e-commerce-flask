from flask_restful import Resource, reqparse
from models.owner import OwnerModel

class OwnerRegister(Resource):
    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('first_name',
                type=str,
                required=True,
                help="fill that part"
        )

        self.parser.add_argument('last_name',
                type=str,
                required=True,
                help="fill that part"
        )

        self.parser.add_argument('username',
                type=str,
                required=True,
                help="fill that part"
        )
        self.parser.add_argument('password',
                type=str,
                required=True,
                help="fill that part"
        )
        self.parser.add_argument('email',
                type=str,
                required=True,
                help="fill that part"
        )
        
        data = self.parser.parse_args()

        if OwnerModel.find_by_username(data['username']):
            return {"message": "owner already exists"}

        owner = OwnerModel(**data)
        owner.save_to_database()

        return {"message": "owner created successfully!"}, 201

class OwnerList(Resource):
    def get(self):
        return {"Owners": [owner.json() for owner in OwnerModel.query.all()]}
