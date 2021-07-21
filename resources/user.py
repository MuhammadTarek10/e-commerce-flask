from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token,
    )

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


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        return user.json(), 200

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="fill that part")
    parser.add_argument("password", type=str, required=True, help="fill that part")

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        return {"message": "wrong username or password"}, 401


class UserList(Resource):
    def get(self):
        return {"Users": [user.json() for user in UserModel.query.all()]}
