from models.user import UserModel


def authentication(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
