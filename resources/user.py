from flask_restful import Resource, reqparse
from models.user import UserModel
from flask import make_response, render_template
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token,
    )
from libs.mailgun import MailGunException

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

        if UserModel.find_by_email(data["email"]):
            return {"message": "email already exists"}

        user = UserModel(**data)
        try:
            user.save_to_database()
            user.send_confirmation_email()
            return {"message": "user created successfully!"}, 201
        except MailGunException as e:
            user.delete_from_database()
            return {"message": str(e)}, 500
        except:
            return {"message": "error in adding to database"}


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
            return {"message": "no user with that usernmae"}
        if user.password == data['password']:
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            return {"message": "account not activated"}
        return {"message": "wrong username or password"}, 401


class UserList(Resource):
    def get(self):
        return {"Users": [user.json() for user in UserModel.query.all()]}

class UserConfirm(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}

        if user.activated:
            return {"message": "already active"}

        user.activated = True
        user.save_to_database()
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=user.email), 200, headers)