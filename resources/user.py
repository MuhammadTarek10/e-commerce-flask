from flask_restful import Resource
from flask import request
from models.user import UserModel
from schemas.user import UserSchema
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token
    )

user_schema = UserSchema()

class UserRegister(Resource):

    def post(cls):
        data = user_schema.load(request.json())

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
        if not user:
            return {"message": "no username found"}

        if user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "wrong inputs"}, 401


class UserList(Resource):
    def get(self):
        return {"Users": [user_schema.dump(user) for user in UserModel.query.all()]}
