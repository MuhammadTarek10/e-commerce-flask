from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = UserModel
		load_only = ("password", "last_name")
		dump_only = ("id", )

