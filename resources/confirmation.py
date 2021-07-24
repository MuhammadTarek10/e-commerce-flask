from time import time

from flask_restful import Resource
from flask import make_response, render_template

from models.confirmation import ConfirmationModel
from models.user import UserModel
from libs.mailgun import MailGunException

class Confirmation(Resource):
    def get(self, confirmation_id):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": "not found"}, 404

        if confirmation.expired:
            return {"message": "confirmation expired"}, 400

        if confirmation.confirmed:
            return {"message": "already confirmed"}, 400

        confirmation.confirmed = True
        confirmation.save_to_database()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_path.html", email=confirmation.user.email),
            200,
            headers
        )

class ConfirmationByUser(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404

        return(
            {
                "current_time": int(time()),
                "confirmation":
                [
                    confirmation.json() for confirmation in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            }, 200
        )

    def post(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": "already confirmed"}, 400
                confrimation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_database()
            user.send_confirmation_email()
            return {"message": "resend successful"}, 201
        except MailGunException as e:
            return {"message": str(e)}, 500
        except:
            return {"message": "resend failed"}, 500