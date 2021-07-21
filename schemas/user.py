from ma import ma
from models.user import UserModel
from models.rate_to_product import RateToProductModel
from models.rate_to_owner import RateToOwnerModel
from models.order import OrderModel
from schemas.order import OrderSchema
from schemas.rate_to_product import RateToProductSchema
from schemas.rate_to_owner import RateToOwnerSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
	rate_to_product = ma.Nested(RateToProductSchema, many=True)
	rate_to_owner = ma.Nested(RateToOwnerSchema, many=True)
	order = ma.Nested(OrderSchema, many=True)
	class Meta:
		model = UserModel
		load_only = ("id", "last_name", "password", )
		include_fk = True