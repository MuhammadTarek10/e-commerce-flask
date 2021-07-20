from flask_restful import Resource, reqparse
from models.user import UserModel
from flask import request
from schemas.user import UserSchema
from marshmallow import ValidationError


parser = reqparse.RequestParser()

user_schema = UserSchema()

class UserRegister(Resource):

    def post(self):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.message, 400

        user = UserModel.find_by_username(user_data['username'])
        email_exists = UserModel.if_email_exists(user_data['email'])


        if user:
            return {"message": "user already exists"}
        if email_exists:
            return {"message": "email already exists"}

        user = UserModel(**user_data)
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
        return user_schema.dump(user), 200



class UserList(Resource):
    def get(self):
        return {"Users": [user_schema.dump(user) for user in UserModel.query.all()]}
