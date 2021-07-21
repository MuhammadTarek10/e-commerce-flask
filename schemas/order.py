from ma import ma
from models.order import OrderModel

class OrderSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		include_fk = True