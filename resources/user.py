from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token,
    )
from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel

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
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_database()
            user.send_confirmation_email()
            return {"message": "a confirmation email has been sent to you, check it out"}, 201
        except MailGunException as e:
            user.delete_from_database()
            return {"message": str(e)}, 500
        except:
            user.delete_from_database()
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
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            return {"message": "account not activated"}
        return {"message": "wrong username or password"}, 401


class UserList(Resource):
    def get(self):
        confirmed_users = []
        all_users = UserModel.query.all()
        for user in all_users:
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                confirmed_users.append(user)
        return {"Users": [user.json() for user in confirmed_users]}