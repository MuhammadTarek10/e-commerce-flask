from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("first_name", type=str, required=True, help="fill that part")

    parser.add_argument("last_name", type=str, required=True, help="fill that part")

    parser.add_argument("username", type=str, required=True, help="fill that part")
    parser.add_argument("password", type=str, required=True, help="fill that part")
    parser.add_argument("email", type=str, required=True, help="fill that part")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "user already exists"}

        user = UserModel(**data)
        try:
            user.save_to_database()
        except:
            return {"message": "error in adding to database"}

        return {"message": "user created successfully!"}, 201


class UserList(Resource):
    def get(self):
        return {"Users": [user.json() for user in UserModel.query.all()]}
